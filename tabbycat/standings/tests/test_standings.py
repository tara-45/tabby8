import logging

from django.test import TestCase

from adjallocation.models import DebateAdjudicator
from draw.models import Debate, DebateTeam
from participants.models import Adjudicator, Institution, Speaker, Team
from results.models import BallotSubmission, SpeakerScore, TeamScore
from tournaments.models import Round, Tournament
from utils.tests import suppress_logs
from venues.models import Venue

from ..base import StandingsError
from ..teams import TeamStandingsGenerator


class TestTrivialStandings(TestCase):
    """Tests cases with just two teams and two rounds.

    Mostly intended to check that it doesn't crash under lots of different
    configurations, rather than check the results of the ordering or aggregation
    functions themselves."""

    def setUp(self):
        self.tournament = Tournament.objects.create(slug="trivialstandingstest", name="Trivial standings test")
        self.team1 = Team.objects.create(tournament=self.tournament, reference="1", use_institution_prefix=False)
        self.team2 = Team.objects.create(tournament=self.tournament, reference="2", use_institution_prefix=False)
        adj = Adjudicator.objects.create(tournament=self.tournament, name="Adjudicator")
        for i in [1, 2]:
            rd = Round.objects.create(tournament=self.tournament, seq=i)
            debate = Debate.objects.create(round=rd, flags=['pullup'])
            dt1 = DebateTeam.objects.create(debate=debate, team=self.team1, side=DebateTeam.Side.AFF, flags=['pullup'])
            dt2 = DebateTeam.objects.create(debate=debate, team=self.team2, side=DebateTeam.Side.NEG)
            DebateAdjudicator.objects.create(debate=debate, adjudicator=adj, type=DebateAdjudicator.TYPE_CHAIR)
            ballotsub = BallotSubmission.objects.create(debate=debate, confirmed=True)
            TeamScore.objects.create(debate_team=dt1, ballot_submission=ballotsub,
                margin=+2*i, points=1, score=100+i, win=True,  votes_given=1, votes_possible=1)
            TeamScore.objects.create(debate_team=dt2, ballot_submission=ballotsub,
                margin=-2*i, points=0, score=100-i, win=False, votes_given=0, votes_possible=1)

    def tearDown(self):
        DebateTeam.objects.filter(team__tournament=self.tournament).delete()
        self.tournament.delete()

    def get_standings(self, generator):
        with suppress_logs('standings.metrics', logging.INFO):
            standings = generator.generate(self.tournament.team_set.all())
        return standings

    def set_up_speaker_scores(self, position):
        speaker1 = Speaker.objects.create(team=self.team1, name="Speaker 1")
        speaker2 = Speaker.objects.create(team=self.team2, name="Speaker 2")
        for i in [1, 2]:
            rd = Round.objects.get(tournament=self.tournament, seq=i)
            dt1 = DebateTeam.objects.get(debate__round=rd, team=self.team1)
            dt2 = DebateTeam.objects.get(debate__round=rd, team=self.team2)
            ballotsub = BallotSubmission.objects.get(debate__round=rd)
            SpeakerScore.objects.create(debate_team=dt1, ballot_submission=ballotsub,
                speaker=speaker1, position=position, score=100+i)
            SpeakerScore.objects.create(debate_team=dt2, ballot_submission=ballotsub,
                speaker=speaker2, position=position, score=100-i)

    def _base_metric_test(self, metrics):
        generator = TeamStandingsGenerator(metrics.keys(), ())
        standings = self.get_standings(generator)
        for mkey, mvalues in metrics.items():
            if isinstance(mvalues, dict):
                key, values = next(iter(mvalues.items()))
            else:
                key, values = mkey, mvalues
            self.assertEqual(standings.get_standing(self.team1).metrics[key], values[0])
            self.assertEqual(standings.get_standing(self.team2).metrics[key], values[1])

    def test_nothing(self):
        # just test that it does not crash
        generator = TeamStandingsGenerator((), ())
        generator.generate(self.tournament.team_set.all())

    def test_no_metrics(self):
        generator = TeamStandingsGenerator((), ('rank', 'subrank'))
        standings = self.get_standings(generator)
        self.assertEqual(standings.get_standing(self.team1).rankings['rank'], (1, True))
        self.assertEqual(standings.get_standing(self.team2).rankings['rank'], (1, True))
        self.assertEqual(standings.get_standing(self.team1).rankings['subrank'], (1, True))
        self.assertEqual(standings.get_standing(self.team2).rankings['subrank'], (1, True))

    def test_only_extra_metrics(self):
        generator = TeamStandingsGenerator((), ('rank', 'subrank'), extra_metrics=('points',))
        standings = self.get_standings(generator)
        self.assertEqual(standings.get_standing(self.team1).rankings['rank'], (1, True))
        self.assertEqual(standings.get_standing(self.team2).rankings['rank'], (1, True))
        self.assertEqual(standings.get_standing(self.team1).rankings['subrank'], (1, True))
        self.assertEqual(standings.get_standing(self.team2).rankings['subrank'], (1, True))

    def test_no_rankings(self):
        self._base_metric_test({'points': [2, 0]})

    def test_wins(self):
        self._base_metric_test({'wins': [2, 0]})

    def test_speaks_sum(self):
        self._base_metric_test({'speaks_sum': [203, 197]})

    def test_speaks_avg(self):
        self._base_metric_test({'speaks_avg': [101.5, 98.5]})

    def test_speaks_ind_avg(self):
        self.set_up_speaker_scores(1)
        self._base_metric_test({'speaks_ind_avg': [101.5, 98.5]})

    def test_speaks_stddev(self):
        self._base_metric_test({'speaks_stddev': [.5, .5]})

    def test_draw_strength(self):
        # losing team has faced winning team twice, so draw strength is 2 * 2 = 4
        self._base_metric_test({'draw_strength': [0, 4]})

    def test_draw_strength_speaks(self):
        # teams have faced each other twice, so draw strength is twice opponent's score
        self._base_metric_test({'draw_strength_speaks': [394, 406]})

    def test_margin_sum(self):
        self._base_metric_test({'margin_sum': [6, -6]})

    def test_margin_avg(self):
        self._base_metric_test({'margin_avg': [3, -3]})

    def test_num_adjs(self):
        # normalized to 3 adjs per debate, so the winning team has 6 adjudicators
        self._base_metric_test({'num_adjs': [6, 0]})

    def test_wbw_not_tied(self):
        self._base_metric_test({'points': [2, 0], 'wbw': {'wbw1': ['n/a', 'n/a']}})

    def test_wbw_first(self):
        # tests wbw when it appears as the first metric
        self._base_metric_test({'wbw': {'wbw1': [2, 0]}})

    def test_wbw_tied(self):
        # firsts should be 0 for both teams as only applicable in BP, so is a tied
        # first metric, allowing wbw to be tested as a second metric (the normal use case)
        self._base_metric_test({'firsts': [0, 0], 'wbw': {'wbw1': [2, 0]}})

    def test_npullups(self):
        self._base_metric_test({'npullups': [2, 0]})

    def test_pullup_debates(self):
        self._base_metric_test({'pullup_debates': [2, 2]})

    def test_pullup_debates_combinable(self):
        self._base_metric_test({'points': [2, 0], 'npullups': [2, 0], 'pullup_debates': [2, 2]})

    def test_points_ranked(self):
        generator = TeamStandingsGenerator(('points',), ('rank',))
        standings = self.get_standings(generator)
        self.assertEqual(standings.get_standing(self.team1).metrics['points'], 2)
        self.assertEqual(standings.get_standing(self.team2).metrics['points'], 0)
        self.assertEqual(standings.get_standing(self.team1).rankings['rank'], (1, False))
        self.assertEqual(standings.get_standing(self.team2).rankings['rank'], (2, False))

    def test_speaks_ranked(self):
        generator = TeamStandingsGenerator(('speaks_sum',), ('rank',))
        standings = self.get_standings(generator)
        self.assertEqual(standings.get_standing(self.team1).metrics['speaks_sum'], 203)
        self.assertEqual(standings.get_standing(self.team2).metrics['speaks_sum'], 197)
        self.assertEqual(standings.get_standing(self.team1).rankings['rank'], (1, False))
        self.assertEqual(standings.get_standing(self.team2).rankings['rank'], (2, False))

    def test_points_speaks_subrank(self):
        generator = TeamStandingsGenerator(('points', 'speaks_sum'), ('rank', 'subrank'))
        standings = self.get_standings(generator)
        self.assertEqual(standings.get_standing(self.team1).metrics['points'], 2)
        self.assertEqual(standings.get_standing(self.team2).metrics['points'], 0)
        self.assertEqual(standings.get_standing(self.team1).metrics['speaks_sum'], 203)
        self.assertEqual(standings.get_standing(self.team2).metrics['speaks_sum'], 197)
        self.assertEqual(standings.get_standing(self.team1).rankings['rank'], (1, False))
        self.assertEqual(standings.get_standing(self.team2).rankings['rank'], (2, False))
        self.assertEqual(standings.get_standing(self.team1).rankings['subrank'], (1, False))
        self.assertEqual(standings.get_standing(self.team2).rankings['subrank'], (1, False))

    def test_double_metric_error(self):
        self.assertRaises(StandingsError, TeamStandingsGenerator, ('points', 'wbw', 'points'), ('rank',))

    def test_points_with_extra_team(self):
        # check that a team with no debates doesn't throw off the rankings
        team_extra = Team.objects.create(tournament=self.tournament, reference="extra", use_institution_prefix=False)
        generator = TeamStandingsGenerator(('points',), ('rank',))
        standings = self.get_standings(generator)
        self.assertEqual(standings.get_standing(self.team1).rankings['rank'], (1, False))
        self.assertEqual(standings.get_standing(self.team2).rankings['rank'], (2, False))
        self.assertEqual(standings.get_standing(team_extra).rankings['rank'], (3, False))

    def test_wins_with_extra_team(self):
        # check that a team with no debates doesn't throw off the rankings
        team_extra = Team.objects.create(tournament=self.tournament, reference="extra", use_institution_prefix=False)
        generator = TeamStandingsGenerator(('wins',), ('rank',))
        standings = self.get_standings(generator)
        self.assertEqual(standings.get_standing(self.team1).rankings['rank'], (1, False))
        self.assertEqual(standings.get_standing(self.team2).rankings['rank'], (2, True))
        self.assertEqual(standings.get_standing(team_extra).rankings['rank'], (2, True))

    def test_noncombinable_metric(self):
        # Check that metrics that add a join do not interfere with other metrics
        self.set_up_speaker_scores(1)
        self.set_up_speaker_scores(2)
        self._base_metric_test({'wins': [2, 0], 'speaks_ind_avg': [101.5, 98.5]})


class IgnorableDebateMixin:

    def set_up_ignorable_debate(self):
        adj = Adjudicator.objects.get()
        rd = Round.objects.create(tournament=self.tournament, seq=3)
        debate = Debate.objects.create(round=rd)
        dt1 = DebateTeam.objects.create(debate=debate, team=self.team1, side=DebateTeam.Side.AFF)
        dt2 = DebateTeam.objects.create(debate=debate, team=self.team2, side=DebateTeam.Side.NEG)
        DebateAdjudicator.objects.create(debate=debate, adjudicator=adj, type=DebateAdjudicator.TYPE_CHAIR)
        ballotsub = BallotSubmission.objects.create(debate=debate, confirmed=True)
        TeamScore.objects.create(debate_team=dt1, ballot_submission=ballotsub,
            margin=-25, points=0, score=300, win=False, votes_given=0, votes_possible=3)
        TeamScore.objects.create(debate_team=dt2, ballot_submission=ballotsub,
            margin=+25, points=1, score=325, win=True,  votes_given=3, votes_possible=3)
        return debate

    def set_up_speaker_scores(self, position):
        super().set_up_speaker_scores(position)
        speaker1 = Speaker.objects.filter(team=self.team1, name="Speaker 1").first()
        speaker2 = Speaker.objects.filter(team=self.team2, name="Speaker 2").first()
        rd = Round.objects.get(tournament=self.tournament, seq=3)
        dt1 = DebateTeam.objects.get(debate__round=rd, team=self.team1)
        dt2 = DebateTeam.objects.get(debate__round=rd, team=self.team2)
        ballotsub = BallotSubmission.objects.get(debate__round=rd)
        SpeakerScore.objects.create(debate_team=dt1, ballot_submission=ballotsub,
            speaker=speaker1, position=position, score=350)
        SpeakerScore.objects.create(debate_team=dt2, ballot_submission=ballotsub,
            speaker=speaker2, position=position, score=375)


class TestStandingsWithEliminationRound(IgnorableDebateMixin, TestTrivialStandings):

    def setUp(self):
        super().setUp()
        debate = self.set_up_ignorable_debate()
        debate.round.stage = Round.Stage.ELIMINATION
        debate.round.save()


class TestStandingsWithUnconfirmedBallotSubmission(IgnorableDebateMixin, TestTrivialStandings):

    def setUp(self):
        super().setUp()
        debate = self.set_up_ignorable_debate()
        debate.ballotsubmission_set.update(confirmed=False)

    def test_draw_strength(self):
        # The ignorable debate still counts as an opponent (because they definitely faced each
        # other) but does not count as a win (because it's unconfirmed). So the losing team has
        # faced the winning team 3 times (including ignorable debate), and the winning team has 2
        # wins (excluding ignorable debate), for a losing team draw strength of 3 * 2 = 6.
        self._base_metric_test({'draw_strength': [0, 6]})

    def test_draw_strength_speaks(self):
        self._base_metric_test({'draw_strength_speaks': [591, 609]})


class TestBasicStandings(TestCase):

    TEAMS = "ABCD"

    testdata = dict()
    testdata[1] = \
        {'rankings': {('points', 'speaks_sum'): ['A', 'D', 'C', 'B'],
                      ('points', 'speaks_sum', 'draw_strength', 'margin_sum'): ['A', 'D', 'C', 'B']},
         'standings': {'A': {'against': {'B': 2, 'C': 0, 'D': 'n/a'},
                             'draw_strength': 2,
                             'margin_sum': 46.0,
                             'points': 2,
                             'speaks_sum': 804.5},
                       'B': {'against': {'A': 0, 'C': 'n/a', 'D': 0},
                             'draw_strength': 6,
                             'margin_sum': -62.0,
                             'points': 0,
                             'speaks_sum': 753.5},
                       'C': {'against': {'A': 1, 'B': 'n/a', 'D': 1},
                             'draw_strength': 6,
                             'margin_sum': 8.0,
                             'points': 2,
                             'speaks_sum': 784.5},
                       'D': {'against': {'A': 'n/a', 'B': 1, 'C': 1},
                             'draw_strength': 4,
                             'margin_sum': 8.0,
                             'points': 2,
                             'speaks_sum': 787.5}},
         'teams': ['A', 'B', 'C', 'D'],
         'teamscores': [{'AB': {'A': {'margin': 22.5,  'points': 1, 'score': 265.0, 'win': True,  'votes_given': 1, 'votes_possible': 1},
                                'B': {'margin': -22.5, 'points': 0, 'score': 242.5, 'win': False, 'votes_given': 0, 'votes_possible': 1}},
                         'CD': {'C': {'margin': 20.0,  'points': 1, 'score': 273.0, 'win': True,  'votes_given': 1, 'votes_possible': 1},
                                'D': {'margin': -20.0, 'points': 0, 'score': 253.0, 'win': False, 'votes_given': 0, 'votes_possible': 1}}},
                        {'AC': {'A': {'margin': -1.5,  'points': 0, 'score': 263.5, 'win': False, 'votes_given': 0, 'votes_possible': 1},
                                'C': {'margin': 1.5,   'points': 1, 'score': 265.0, 'win': True,  'votes_given': 1, 'votes_possible': 1}},
                         'BD': {'B': {'margin': -14.5, 'points': 0, 'score': 260.0, 'win': False, 'votes_given': 0, 'votes_possible': 1},
                                'D': {'margin': 14.5,  'points': 1, 'score': 274.5, 'win': True,  'votes_given': 1, 'votes_possible': 1}}},
                        {'AB': {'A': {'margin': 25.0,  'points': 1, 'score': 276.0, 'win': True,  'votes_given': 1, 'votes_possible': 1},
                                'B': {'margin': -25.0, 'points': 0, 'score': 251.0, 'win': False, 'votes_given': 0, 'votes_possible': 1}},
                         'CD': {'C': {'margin': -13.5, 'points': 0, 'score': 246.5, 'win': False, 'votes_given': 0, 'votes_possible': 1},
                                'D': {'margin': 13.5,  'points': 1, 'score': 260.0, 'win': True,  'votes_given': 1, 'votes_possible': 1}}}]}

    rankings = ('rank',)

    def setup_testdata(self, testdata):
        tournament = Tournament.objects.create(slug="basicstandingstest", name="Basic standings test")
        teams = dict()
        for team_name in testdata["teams"]:
            inst = Institution.objects.create(code=team_name, name=team_name)
            team = Team.objects.create(tournament=tournament, institution=inst, reference=team_name, use_institution_prefix=False)
            teams[team_name] = team
        inst = Institution.objects.create(code="Adjs", name="Adjudicators")
        for i in range(len(testdata["teams"])//2):
            Adjudicator.objects.create(tournament=tournament, institution=inst, name="Adjudicator {:d}".format(i), base_score=5)
            Venue.objects.create(name="Venue {:d}".format(i), priority=10)
        adjs = list(Adjudicator.objects.all())
        venues = list(Venue.objects.all())
        sides = [DebateTeam.Side.AFF, DebateTeam.Side.NEG]

        for r, debatedict in enumerate(testdata["teamscores"]):
            rd = Round.objects.create(tournament=tournament, seq=r, abbreviation="R{:d}".format(r))
            for adj, venue, (teamnames, teamscores) in zip(adjs, venues, debatedict.items()):
                debate = Debate.objects.create(round=rd, venue=venue)
                for team, side in zip(teamnames, sides):
                    DebateTeam.objects.create(debate=debate, team=teams[team], side=side)
                DebateAdjudicator.objects.create(debate=debate, adjudicator=adj, type=DebateAdjudicator.TYPE_CHAIR)
                ballotsub = BallotSubmission.objects.create(debate=debate, confirmed=True)
                for team, teamscore_dict in teamscores.items():
                    dt = DebateTeam.objects.get(debate=debate, team=teams[team])
                    TeamScore.objects.create(debate_team=dt, ballot_submission=ballotsub, **teamscore_dict)

        return tournament, teams

    def teardown_testdata(self, tournament):
        tournament.delete()

    def test_standings(self):
        for index, testdata in self.testdata.items():
            tournament, teams = self.setup_testdata(testdata)
            for metrics in testdata["rankings"].keys():
                with self.subTest(index=index, metrics=metrics):
                    generator = TeamStandingsGenerator(metrics, self.rankings)
                    with suppress_logs('standings.teams', logging.INFO), \
                            suppress_logs('standings.metrics', logging.INFO):
                        standings = generator.generate(tournament.team_set.all())

                    self.assertEqual(len(standings), len(testdata["standings"]))
                    self.assertEqual(standings.metric_keys, list(metrics))

                    for teamname, expected in testdata["standings"].items():
                        team = teams[teamname]
                        standing = standings.get_standing(team)
                        for metric in metrics:
                            self.assertEqual(standing.metrics[metric], expected[metric])

                    ranked_teams = [teams[x] for x in testdata["rankings"][metrics]]
                    self.assertEqual(ranked_teams, standings.get_instance_list())

    # TODO check that WBW is correct when not in first metrics
    # TODO check that it doesn't break when not all metrics present
    # TODO check that it works for different rounds


class TestMissingStandings(TestCase):

    def setUp(self):
        self.tournament = Tournament.objects.create(slug="missingstandingstest", name="Missing standings test")
        self.team1 = Team.objects.create(tournament=self.tournament, reference="1", use_institution_prefix=False)
        self.team2 = Team.objects.create(tournament=self.tournament, reference="2", use_institution_prefix=False)

    def tearDown(self):
        self.tournament.delete()

    def get_standings(self, generator):
        with suppress_logs('standings.metrics', logging.INFO):
            return generator.generate(self.tournament.team_set.all())

    def test_num_adjs_missing(self):
        generator = TeamStandingsGenerator(('num_adjs',), ())
        standings = self.get_standings(generator)
        self.assertEqual(standings.get_standing(self.team1).metrics['num_adjs'], 0)
        self.assertEqual(standings.get_standing(self.team2).metrics['num_adjs'], 0)
