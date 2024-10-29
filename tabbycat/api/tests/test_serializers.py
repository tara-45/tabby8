import logging

from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, APITestCase

from adjallocation.models import DebateAdjudicator
from draw.models import Debate, DebateTeam
from motions.models import Motion, RoundMotion
from options.presets import CanadianParliamentaryPreferences
from participants.models import Adjudicator, Speaker, Team
from tournaments.models import Round, Tournament
from utils.misc import reverse_round, reverse_tournament
from utils.tests import CompletedTournamentTestMixin

User = get_user_model()


class RoundSerializerTests(CompletedTournamentTestMixin, APITestCase):

    def test_exclude_motions_if_list(self):
        response = self.client.get(reverse_tournament('api-round-list', self.tournament))
        self.assertIsNone(response.data[0].get('motions'))

    def test_include_motions_if_released(self):
        round = self.tournament.round_set.first()
        round.motions_released = True
        round.save()

        response = self.client.get(reverse_round('api-round-detail', self.tournament.round_set.first()))
        self.assertEqual(len(response.data.get('motions')), 3)

    def test_exclude_feedback_weight_public(self):
        response = self.client.get(reverse_tournament('api-round-list', self.tournament))
        self.assertIsNone(response.data[0].get('feedback_weight'))

    def test_include_feedback_weight_admin(self):
        self.client.login(username="admin", password="admin")
        response = self.client.get(reverse_tournament('api-round-list', self.tournament))
        self.assertIsNotNone(response.data[0].get('feedback_weight'))

    def test_seq_validation(self):
        client = APIClient()
        client.login(username="admin", password="admin")
        response = client.post(reverse_tournament('api-round-list', self.tournament), {
            'motions': [],
            'seq': 1,
            'name': 'Round 1',
            'abbreviation': 'R1',
            'draw_type': 'R',
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['seq'][0], 'Object with same value exists in the tournament')

    def test_break_category_validation(self):
        client = APIClient()
        client.login(username="admin", password="admin")
        round = self.tournament.round_set.filter(stage=Round.Stage.ELIMINATION).first()
        response = client.patch(reverse_round('api-round-detail', round), {
            'break_category': None,
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['non_field_errors'][0], 'Rounds are elimination iff they have a break category.')

    def test_can_create_round(self):
        client = APIClient()
        client.login(username="admin", password="admin")
        self.tournament.round_set.get(seq=5).delete()
        response = client.post(reverse_tournament('api-round-list', self.tournament), {
            'motions': [{
                'text': 'THW test code',
                'reference': 'Test',
                'seq': 1,
            }],
            'seq': 5,
            'name': 'Round 5',
            'abbreviation': 'R5',
            'draw_type': 'P',
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(response.data['motions']), 1)

    def test_can_update_round_motion(self):
        client = APIClient()
        client.login(username="admin", password="admin")
        round = self.tournament.round_set.get(seq=5)
        round.roundmotion_set.all().delete()
        motion = round.prev.motion_set.first()
        response = client.patch(reverse_round('api-round-detail', round), {
            'motions': [
                {
                    'pk': motion.id,
                    'text': motion.text,
                    'reference': 'Test',
                },
                {
                    'text': 'THW write tests',
                    'reference': 'Unit Test',
                },
            ],
            'name': 'Round Five',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Round Five')


class MotionSerializerTests(CompletedTournamentTestMixin, APITestCase):

    def test_create_motion_with_round(self):
        client = APIClient()
        client.login(username="admin", password="admin")
        response = client.post(reverse_tournament('api-motion-list', self.tournament), {
            'text': 'This House would straighten all bananas',
            'reference': 'Bananas',
            'info_slide': 'Get bent',
            'rounds': [{'seq': 4, 'round': 'http://testserver/api/v1/tournaments/demo/rounds/1'}],
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(response.data['rounds']), 1)


class AdjudicatorSerializerTests(CompletedTournamentTestMixin, APITestCase):

    def test_create_adj_null_institution(self):
        client = APIClient()
        client.login(username="admin", password="admin")
        response = client.post(reverse_tournament('api-adjudicator-list', self.tournament), {
            "name": "string",
            "gender": "M",
            "email": "user@example.com",
            "phone": "string",
            "anonymous": True,
            "pronoun": "string",
            "institution": None,
            "base_score": 0,
            "breaking": False,
            "trainee": False,
            "independent": True,
            "adj_core": False,
            "institution_conflicts": [],
            "team_conflicts": [],
            "adjudicator_conflicts": [],
            "url_key": "laZzBPo6FsGEr12VtB8LSHM8",
        })
        self.assertEqual(response.status_code, 201)


class BallotSerializerTests(APITestCase):

    def setUp(self):
        logging.disable(logging.CRITICAL)
        self.user = User.objects.create_superuser(username='admin1', password='admin', is_active=True)
        self.tournament = Tournament.objects.create(slug='apitest')
        self.round = Round.objects.create(seq=1, tournament=self.tournament)
        self.debate = Debate.objects.create(round=self.round)

        CanadianParliamentaryPreferences.save(self.tournament)

        self.t1 = Team.objects.create(tournament=self.tournament, reference='A')
        self.s1 = Speaker.objects.create(name='1', team=self.t1)
        self.s2 = Speaker.objects.create(name='2', team=self.t1)

        self.t2 = Team.objects.create(tournament=self.tournament, reference='B')
        self.s3 = Speaker.objects.create(name='3', team=self.t2)
        self.s4 = Speaker.objects.create(name='4', team=self.t2)

        self.t3 = Team.objects.create(tournament=self.tournament, reference='C')

        self.a1 = Adjudicator.objects.create(name='A1', tournament=self.tournament)
        self.a2 = Adjudicator.objects.create(name='A2', tournament=self.tournament)
        self.a3 = Adjudicator.objects.create(name='A3', tournament=self.tournament)

        DebateTeam.objects.bulk_create([DebateTeam(side=side, team=team, debate=self.debate) for side, team in zip(['aff', 'neg'], [self.t1, self.t2])])
        DebateAdjudicator.objects.bulk_create([
            DebateAdjudicator(adjudicator=self.a1, debate=self.debate, type='C'), DebateAdjudicator(adjudicator=self.a2, debate=self.debate, type='P'),
        ])

        self.m1 = Motion.objects.create(tournament=self.tournament)
        self.m2 = Motion.objects.create(tournament=self.tournament)
        self.m3 = Motion.objects.create(tournament=self.tournament)
        RoundMotion.objects.bulk_create([RoundMotion(seq=i, motion=motion, round=self.round) for i, motion in enumerate([self.m1, self.m2])])

    def tearDown(self):
        self.debate.delete()
        self.tournament.delete()
        self.user.delete()
        logging.disable(logging.NOTSET)

    def test_can_create_consensus_ballot_scores(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.post(reverse_round('api-ballot-list', self.round, kwargs={'debate_pk': self.debate.pk}), {
            'result': {
                'sheets': [{
                    'teams': [
                        {
                            'side': 'aff',
                            'team': reverse_tournament('api-team-detail', self.tournament, kwargs={'pk': self.t1.pk}),
                            'speeches': [
                                {
                                    'ghost': False,
                                    'score': 80,
                                    'speaker': reverse_tournament('api-speaker-detail', self.tournament, kwargs={'pk': self.s1.pk}),
                                },
                                {
                                    'ghost': False,
                                    'score': 80,
                                    'speaker': reverse_tournament('api-speaker-detail', self.tournament, kwargs={'pk': self.s2.pk}),
                                },
                            ],
                        },
                        {
                            'side': 'neg',
                            'team': reverse_tournament('api-team-detail', self.tournament, kwargs={'pk': self.t2.pk}),
                            'speeches': [
                                {
                                    'ghost': False,
                                    'score': 79,
                                    'speaker': reverse_tournament('api-speaker-detail', self.tournament, kwargs={'pk': self.s3.pk}),
                                },
                                {
                                    'ghost': False,
                                    'score': 79,
                                    'speaker': reverse_tournament('api-speaker-detail', self.tournament, kwargs={'pk': self.s4.pk}),
                                },
                            ],
                        },
                    ],
                }],
            },
        })
        self.assertEqual(response.status_code, 201)

    def test_can_create_voting_ballot_scores(self):
        self.tournament.preferences['debate_rules__ballots_per_debate_prelim'] = 'per-adj'

        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.post(reverse_round('api-ballot-list', self.round, kwargs={'debate_pk': self.debate.pk}), {
            'result': {
                'sheets': [
                    {
                        'adjudicator': reverse_tournament('api-adjudicator-detail', self.tournament, kwargs={'pk': self.a1.pk}),
                        'teams': [
                            {
                                'side': 'aff',
                                'team': reverse_tournament('api-team-detail', self.tournament, kwargs={'pk': self.t1.pk}),
                                'speeches': [
                                    {
                                        'ghost': False,
                                        'score': 80,
                                        'speaker': reverse_tournament('api-speaker-detail', self.tournament, kwargs={'pk': self.s1.pk}),
                                    },
                                    {
                                        'ghost': False,
                                        'score': 80,
                                        'speaker': reverse_tournament('api-speaker-detail', self.tournament, kwargs={'pk': self.s2.pk}),
                                    },
                                ],
                            },
                            {
                                'side': 'neg',
                                'team': reverse_tournament('api-team-detail', self.tournament, kwargs={'pk': self.t2.pk}),
                                'speeches': [
                                    {
                                        'ghost': False,
                                        'score': 79,
                                        'speaker': reverse_tournament('api-speaker-detail', self.tournament, kwargs={'pk': self.s3.pk}),
                                    },
                                    {
                                        'ghost': False,
                                        'score': 79,
                                        'speaker': reverse_tournament('api-speaker-detail', self.tournament, kwargs={'pk': self.s4.pk}),
                                    },
                                ],
                            },
                        ],
                    },
                    {
                        'adjudicator': reverse_tournament('api-adjudicator-detail', self.tournament, kwargs={'pk': self.a2.pk}),
                        'teams': [
                            {
                                'side': 'aff',
                                'team': reverse_tournament('api-team-detail', self.tournament, kwargs={'pk': self.t1.pk}),
                                'speeches': [
                                    {
                                        'ghost': False,
                                        'score': 79,
                                        'speaker': reverse_tournament('api-speaker-detail', self.tournament, kwargs={'pk': self.s1.pk}),
                                    },
                                    {
                                        'ghost': False,
                                        'score': 79,
                                        'speaker': reverse_tournament('api-speaker-detail', self.tournament, kwargs={'pk': self.s2.pk}),
                                    },
                                ],
                            },
                            {
                                'side': 'neg',
                                'team': reverse_tournament('api-team-detail', self.tournament, kwargs={'pk': self.t2.pk}),
                                'speeches': [
                                    {
                                        'ghost': False,
                                        'score': 80,
                                        'speaker': reverse_tournament('api-speaker-detail', self.tournament, kwargs={'pk': self.s3.pk}),
                                    },
                                    {
                                        'ghost': False,
                                        'score': 80,
                                        'speaker': reverse_tournament('api-speaker-detail', self.tournament, kwargs={'pk': self.s4.pk}),
                                    },
                                ],
                            },
                        ],
                    },
                ],
            },
        })
        self.assertEqual(response.status_code, 201)

    def test_can_create_consensus_ballot_winner(self):
        self.tournament.preferences['debate_rules__speakers_in_ballots'] = 'never'

        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.post(reverse_round('api-ballot-list', self.round, kwargs={'debate_pk': self.debate.pk}), {
            'result': {
                'sheets': [{
                    'teams': [
                        {
                            'side': 'aff',
                            'team': reverse_tournament('api-team-detail', self.tournament, kwargs={'pk': self.t1.pk}),
                            'win': True,
                        },
                        {
                            'side': 'neg',
                            'team': reverse_tournament('api-team-detail', self.tournament, kwargs={'pk': self.t2.pk}),
                            'win': False,
                        },
                    ],
                }],
            },
        })
        self.assertEqual(response.status_code, 201)

    def test_can_create_voting_ballot_winner(self):
        self.tournament.preferences['debate_rules__ballots_per_debate_prelim'] = 'per-adj'
        self.tournament.preferences['debate_rules__speakers_in_ballots'] = 'never'

        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.post(reverse_round('api-ballot-list', self.round, kwargs={'debate_pk': self.debate.pk}), {
            'result': {
                'sheets': [
                    {
                        'adjudicator': reverse_tournament('api-adjudicator-detail', self.tournament, kwargs={'pk': self.a1.pk}),
                        'teams': [
                            {
                                'side': 'aff',
                                'team': reverse_tournament('api-team-detail', self.tournament, kwargs={'pk': self.t1.pk}),
                                'win': True,
                            },
                            {
                                'side': 'neg',
                                'team': reverse_tournament('api-team-detail', self.tournament, kwargs={'pk': self.t2.pk}),
                                'win': False,
                            },
                        ],
                    },
                    {
                        'adjudicator': reverse_tournament('api-adjudicator-detail', self.tournament, kwargs={'pk': self.a2.pk}),
                        'teams': [
                            {
                                'side': 'aff',
                                'team': reverse_tournament('api-team-detail', self.tournament, kwargs={'pk': self.t1.pk}),
                                'win': False,
                            },
                            {
                                'side': 'neg',
                                'team': reverse_tournament('api-team-detail', self.tournament, kwargs={'pk': self.t2.pk}),
                                'win': True,
                            },
                        ],
                    },
                ],
            },
        })
        self.assertEqual(response.status_code, 201)

    def test_voting_motion_vetos(self):
        self.tournament.preferences['debate_rules__speakers_in_ballots'] = 'never'
        self.tournament.preferences['motions__motion_vetoes_enabled'] = True

        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.post(reverse_round('api-ballot-list', self.round, kwargs={'debate_pk': self.debate.pk}), {
            'result': {
                'sheets': [{
                    'teams': [
                        {
                            'side': 'aff',
                            'team': reverse_tournament('api-team-detail', self.tournament, kwargs={'pk': self.t1.pk}),
                            'win': True,
                        },
                        {
                            'side': 'neg',
                            'team': reverse_tournament('api-team-detail', self.tournament, kwargs={'pk': self.t2.pk}),
                            'win': False,
                        },
                    ],
                }],
            },
            'vetos': [
                {
                    'team': reverse_tournament('api-team-detail', self.tournament, kwargs={'pk': self.t1.pk}),
                    'motion': reverse_tournament('api-motion-detail', self.tournament, kwargs={'pk': self.m1.pk}),
                },
                {
                    'team': reverse_tournament('api-team-detail', self.tournament, kwargs={'pk': self.t2.pk}),
                    'motion': reverse_tournament('api-motion-detail', self.tournament, kwargs={'pk': self.m2.pk}),
                },
            ],
        })
        self.assertEqual(response.status_code, 201)

    def test_single_adj_ballot(self):
        self.tournament.preferences['debate_rules__ballots_per_debate_prelim'] = 'per-adj'
        self.tournament.preferences['debate_rules__speakers_in_ballots'] = 'never'

        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.post(reverse_round('api-ballot-list', self.round, kwargs={'debate_pk': self.debate.pk}), {
            'result': {
                'sheets': [{
                    'adjudicator': reverse_tournament('api-adjudicator-detail', self.tournament, kwargs={'pk': self.a1.pk}),
                    'teams': [
                        {
                            'side': 'aff',
                            'team': reverse_tournament('api-team-detail', self.tournament, kwargs={'pk': self.t1.pk}),
                            'win': True,
                        },
                        {
                            'side': 'neg',
                            'team': reverse_tournament('api-team-detail', self.tournament, kwargs={'pk': self.t2.pk}),
                            'win': False,
                        },
                    ],
                }],
            },
        })
        self.assertEqual(response.status_code, 201)

    def test_team_not_in_debate(self):
        self.tournament.preferences['debate_rules__speakers_in_ballots'] = 'never'

        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.post(reverse_round('api-ballot-list', self.round, kwargs={'debate_pk': self.debate.pk}), {
            'result': {
                'sheets': [{
                    'teams': [
                        {
                            'side': 'aff',
                            'team': reverse_tournament('api-team-detail', self.tournament, kwargs={'pk': self.t2.pk}),
                            'win': True,
                        },
                        {
                            'side': 'neg',
                            'team': reverse_tournament('api-team-detail', self.tournament, kwargs={'pk': self.t3.pk}),
                            'win': False,
                        },
                    ],
                }],
            },
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(str(response.data['result']['sheets'][0]['teams'][0]), 'Inconsistent team')

    def test_team_not_in_correct_side(self):
        self.tournament.preferences['debate_rules__speakers_in_ballots'] = 'never'

        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.post(reverse_round('api-ballot-list', self.round, kwargs={'debate_pk': self.debate.pk}), {
            'result': {
                'sheets': [{
                    'teams': [
                        {
                            'side': 'aff',
                            'team': reverse_tournament('api-team-detail', self.tournament, kwargs={'pk': self.t2.pk}),
                            'win': True,
                        },
                        {
                            'side': 'neg',
                            'team': reverse_tournament('api-team-detail', self.tournament, kwargs={'pk': self.t1.pk}),
                            'win': False,
                        },
                    ],
                }],
            },
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(str(response.data['result']['sheets'][0]['teams'][0]), 'Inconsistent team')

    def test_team_not_in_debate_veto(self):
        self.tournament.preferences['debate_rules__speakers_in_ballots'] = 'never'
        self.tournament.preferences['motions__motion_vetoes_enabled'] = True

        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.post(reverse_round('api-ballot-list', self.round, kwargs={'debate_pk': self.debate.pk}), {
            'result': {
                'sheets': [{
                    'teams': [
                        {
                            'side': 'aff',
                            'team': reverse_tournament('api-team-detail', self.tournament, kwargs={'pk': self.t1.pk}),
                            'win': True,
                        },
                        {
                            'side': 'neg',
                            'team': reverse_tournament('api-team-detail', self.tournament, kwargs={'pk': self.t2.pk}),
                            'win': False,
                        },
                    ],
                }],
            },
            'vetos': [
                {
                    'team': reverse_tournament('api-team-detail', self.tournament, kwargs={'pk': self.t3.pk}),
                    'motion': reverse_tournament('api-motion-detail', self.tournament, kwargs={'pk': self.m1.pk}),
                },
                {
                    'team': reverse_tournament('api-team-detail', self.tournament, kwargs={'pk': self.t2.pk}),
                    'motion': reverse_tournament('api-motion-detail', self.tournament, kwargs={'pk': self.m2.pk}),
                },
            ],
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(str(response.data[0]), 'Team is not in debate')

    def test_adj_not_in_debate(self):
        self.tournament.preferences['debate_rules__ballots_per_debate_prelim'] = 'per-adj'
        self.tournament.preferences['debate_rules__speakers_in_ballots'] = 'never'

        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.post(reverse_round('api-ballot-list', self.round, kwargs={'debate_pk': self.debate.pk}), {
            'result': {
                'sheets': [{
                    'adjudicator': reverse_tournament('api-adjudicator-detail', self.tournament, kwargs={'pk': self.a3.pk}),
                    'teams': [
                        {
                            'side': 'aff',
                            'team': reverse_tournament('api-team-detail', self.tournament, kwargs={'pk': self.t1.pk}),
                            'win': True,
                        },
                        {
                            'side': 'neg',
                            'team': reverse_tournament('api-team-detail', self.tournament, kwargs={'pk': self.t2.pk}),
                            'win': False,
                        },
                    ],
                }],
            },
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(str(response.data['result']['sheets'][0]['adjudicator'][0]), 'Adjudicator must be in debate')

    def test_single_adj_many_ballots_fail(self):
        self.tournament.preferences['debate_rules__ballots_per_debate_prelim'] = 'per-adj'
        self.tournament.preferences['debate_rules__speakers_in_ballots'] = 'never'

        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.post(reverse_round('api-ballot-list', self.round, kwargs={'debate_pk': self.debate.pk}), {
            'single_adj': True,
            'result': {
                'sheets': [
                    {
                        'adjudicator': reverse_tournament('api-adjudicator-detail', self.tournament, kwargs={'pk': self.a1.pk}),
                        'teams': [
                            {
                                'side': 'aff',
                                'team': reverse_tournament('api-team-detail', self.tournament, kwargs={'pk': self.t1.pk}),
                                'win': True,
                            },
                            {
                                'side': 'neg',
                                'team': reverse_tournament('api-team-detail', self.tournament, kwargs={'pk': self.t2.pk}),
                                'win': False,
                            },
                        ],
                    },
                    {
                        'adjudicator': reverse_tournament('api-adjudicator-detail', self.tournament, kwargs={'pk': self.a2.pk}),
                        'teams': [
                            {
                                'side': 'aff',
                                'team': reverse_tournament('api-team-detail', self.tournament, kwargs={'pk': self.t1.pk}),
                                'win': False,
                            },
                            {
                                'side': 'neg',
                                'team': reverse_tournament('api-team-detail', self.tournament, kwargs={'pk': self.t2.pk}),
                                'win': True,
                            },
                        ],
                    },
                ],
            },
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(str(response.data['single_adj']), 'Single-adjudicator ballots can only have one scoresheet')

    def test_incomplete_ballots_fail(self):
        self.tournament.preferences['debate_rules__ballots_per_debate_prelim'] = 'per-adj'
        self.tournament.preferences['debate_rules__speakers_in_ballots'] = 'never'
        DebateAdjudicator.objects.create(adjudicator=self.a3, type=DebateAdjudicator.TYPE_PANEL, debate=self.debate)

        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.post(reverse_round('api-ballot-list', self.round, kwargs={'debate_pk': self.debate.pk}), {
            'result': {
                'sheets': [
                    {
                        'adjudicator': reverse_tournament('api-adjudicator-detail', self.tournament, kwargs={'pk': self.a1.pk}),
                        'teams': [
                            {
                                'side': 'aff',
                                'team': reverse_tournament('api-team-detail', self.tournament, kwargs={'pk': self.t1.pk}),
                                'win': True,
                            },
                            {
                                'side': 'neg',
                                'team': reverse_tournament('api-team-detail', self.tournament, kwargs={'pk': self.t2.pk}),
                                'win': False,
                            },
                        ],
                    },
                    {
                        'adjudicator': reverse_tournament('api-adjudicator-detail', self.tournament, kwargs={'pk': self.a2.pk}),
                        'teams': [
                            {
                                'side': 'aff',
                                'team': reverse_tournament('api-team-detail', self.tournament, kwargs={'pk': self.t1.pk}),
                                'win': False,
                            },
                            {
                                'side': 'neg',
                                'team': reverse_tournament('api-team-detail', self.tournament, kwargs={'pk': self.t2.pk}),
                                'win': True,
                            },
                        ],
                    },
                ],
            },
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(str(response.data['result']), 'Voting ballots must either have one scoresheet or ballots from all voting adjudicators')

    def test_many_ballots_consensus_fail(self):
        self.tournament.preferences['debate_rules__speakers_in_ballots'] = 'never'

        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.post(reverse_round('api-ballot-list', self.round, kwargs={'debate_pk': self.debate.pk}), {
            'result': {
                'sheets': [
                    {
                        'adjudicator': reverse_tournament('api-adjudicator-detail', self.tournament, kwargs={'pk': self.a1.pk}),
                        'teams': [
                            {
                                'side': 'aff',
                                'team': reverse_tournament('api-team-detail', self.tournament, kwargs={'pk': self.t1.pk}),
                                'win': True,
                            },
                            {
                                'side': 'neg',
                                'team': reverse_tournament('api-team-detail', self.tournament, kwargs={'pk': self.t2.pk}),
                                'win': False,
                            },
                        ],
                    },
                    {
                        'adjudicator': reverse_tournament('api-adjudicator-detail', self.tournament, kwargs={'pk': self.a2.pk}),
                        'teams': [
                            {
                                'side': 'aff',
                                'team': reverse_tournament('api-team-detail', self.tournament, kwargs={'pk': self.t1.pk}),
                                'win': False,
                            },
                            {
                                'side': 'neg',
                                'team': reverse_tournament('api-team-detail', self.tournament, kwargs={'pk': self.t2.pk}),
                                'win': True,
                            },
                        ],
                    },
                ],
            },
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(str(response.data['result']), 'Consensus ballots can only have one scoresheet')

    def test_inconsistent_speaker_order(self):
        self.tournament.preferences['debate_rules__ballots_per_debate_prelim'] = 'per-adj'

        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.post(reverse_round('api-ballot-list', self.round, kwargs={'debate_pk': self.debate.pk}), {
            'result': {
                'sheets': [
                    {
                        'adjudicator': reverse_tournament('api-adjudicator-detail', self.tournament, kwargs={'pk': self.a1.pk}),
                        'teams': [
                            {
                                'side': 'aff',
                                'team': reverse_tournament('api-team-detail', self.tournament, kwargs={'pk': self.t1.pk}),
                                'speeches': [
                                    {
                                        'ghost': False,
                                        'score': 80,
                                        'speaker': reverse_tournament('api-speaker-detail', self.tournament, kwargs={'pk': self.s1.pk}),
                                    },
                                    {
                                        'ghost': False,
                                        'score': 80,
                                        'speaker': reverse_tournament('api-speaker-detail', self.tournament, kwargs={'pk': self.s2.pk}),
                                    },
                                ],
                            },
                            {
                                'side': 'neg',
                                'team': reverse_tournament('api-team-detail', self.tournament, kwargs={'pk': self.t2.pk}),
                                'speeches': [
                                    {
                                        'ghost': False,
                                        'score': 79,
                                        'speaker': reverse_tournament('api-speaker-detail', self.tournament, kwargs={'pk': self.s3.pk}),
                                    },
                                    {
                                        'ghost': False,
                                        'score': 79,
                                        'speaker': reverse_tournament('api-speaker-detail', self.tournament, kwargs={'pk': self.s4.pk}),
                                    },
                                ],
                            },
                        ],
                    },
                    {
                        'adjudicator': reverse_tournament('api-adjudicator-detail', self.tournament, kwargs={'pk': self.a2.pk}),
                        'teams': [
                            {
                                'side': 'aff',
                                'team': reverse_tournament('api-team-detail', self.tournament, kwargs={'pk': self.t1.pk}),
                                'speeches': [
                                    {
                                        'ghost': False,
                                        'score': 79,
                                        'speaker': reverse_tournament('api-speaker-detail', self.tournament, kwargs={'pk': self.s2.pk}),
                                    },
                                    {
                                        'ghost': False,
                                        'score': 79,
                                        'speaker': reverse_tournament('api-speaker-detail', self.tournament, kwargs={'pk': self.s1.pk}),
                                    },
                                ],
                            },
                            {
                                'side': 'neg',
                                'team': reverse_tournament('api-team-detail', self.tournament, kwargs={'pk': self.t2.pk}),
                                'speeches': [
                                    {
                                        'ghost': False,
                                        'score': 80,
                                        'speaker': reverse_tournament('api-speaker-detail', self.tournament, kwargs={'pk': self.s3.pk}),
                                    },
                                    {
                                        'ghost': False,
                                        'score': 80,
                                        'speaker': reverse_tournament('api-speaker-detail', self.tournament, kwargs={'pk': self.s4.pk}),
                                    },
                                ],
                            },
                        ],
                    },
                ],
            },
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(str(response.data['result']['non_field_errors'][0]), 'Inconsistant speaker order')

    def test_speaks_without_scores(self):
        self.tournament.preferences['debate_rules__speakers_in_ballots'] = 'never'

        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.post(reverse_round('api-ballot-list', self.round, kwargs={'debate_pk': self.debate.pk}), {
            'result': {
                'sheets': [{
                    'teams': [
                        {
                            'side': 'aff',
                            'team': reverse_tournament('api-team-detail', self.tournament, kwargs={'pk': self.t1.pk}),
                            'win': True,
                            'score': 1,
                        },
                        {
                            'side': 'neg',
                            'team': reverse_tournament('api-team-detail', self.tournament, kwargs={'pk': self.t2.pk}),
                            'win': False,
                            'score': 0,
                        },
                    ],
                }],
            },
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(str(response.data['result']['sheets'][0]['teams'][0]['non_field_errors'][0]), 'Speeches are required to assign scores.')

    def test_inconsistent_speaks(self):
        self.tournament.preferences['debate_rules__speakers_in_ballots'] = 'never'

        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.post(reverse_round('api-ballot-list', self.round, kwargs={'debate_pk': self.debate.pk}), {
            'result': {
                'sheets': [{
                    'teams': [
                        {
                            'side': 'aff',
                            'team': reverse_tournament('api-team-detail', self.tournament, kwargs={'pk': self.t1.pk}),
                            'win': True,
                            'score': 1,
                            'speeches': [
                                {
                                    'ghost': False,
                                    'score': 80,
                                    'speaker': reverse_tournament('api-speaker-detail', self.tournament, kwargs={'pk': self.s1.pk}),
                                },
                                {
                                    'ghost': False,
                                    'score': 80,
                                    'speaker': reverse_tournament('api-speaker-detail', self.tournament, kwargs={'pk': self.s2.pk}),
                                },
                            ],
                        },
                        {
                            'side': 'neg',
                            'team': reverse_tournament('api-team-detail', self.tournament, kwargs={'pk': self.t2.pk}),
                            'win': False,
                            'score': 0,
                            'speeches': [
                                {
                                    'ghost': False,
                                    'score': 79,
                                    'speaker': reverse_tournament('api-speaker-detail', self.tournament, kwargs={'pk': self.s3.pk}),
                                },
                                {
                                    'ghost': False,
                                    'score': 79,
                                    'speaker': reverse_tournament('api-speaker-detail', self.tournament, kwargs={'pk': self.s4.pk}),
                                },
                            ],
                        },
                    ],
                }],
            },
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(str(response.data['result']['sheets'][0]['teams'][0]['non_field_errors'][0]), 'Score must be the sum of speech scores.')
