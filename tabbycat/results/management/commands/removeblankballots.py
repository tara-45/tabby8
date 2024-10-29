from django.db.models import Exists, OuterRef

from utils.management.base import TournamentCommand

from ...models import BallotSubmission, SpeakerScoreByAdj


class Command(TournamentCommand):

    help = "Removes all blank ballot submissions, i.e. ones without adjudicator speaker scores attached."

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument("--dry-run", action="store_true", help="Show what it would delete, but do not actually delete")

    def handle_tournament(self, tournament, **options):
        qs = BallotSubmission.objects.filter(debate__round__tournament=tournament).exclude(
            Exists(SpeakerScoreByAdj.objects.filter(ballot_submission=OuterRef('pk'))))
        for bsub in qs:
            if not options["dry_run"]:
                self.stdout.write("Deleting {:s}".format(str(bsub)))
            else:
                self.stdout.write("Would delete {:s}".format(str(bsub)))
        if not options["dry_run"]:
            qs.delete()
