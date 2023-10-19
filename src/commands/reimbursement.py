import slackutils as slack
import os

def command(channel, user, argument, output):
    slack.respond_to(channel, user, "Reimbursement form: " + os.environ.get("REIMBURSEMENT_FORM")
               + "\nGuidelines: " + os.environ.get("REIMBURSEMENT_FORM_GUIDELINES"))