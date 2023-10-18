
def command_reimbursement(channel, user):
    respond_to(channel, user, "Reimbursement form: " + os.environ.get("REIMBURSEMENT_FORM")
               + "\nGuidelines: " + os.environ.get("REIMBURSEMENT_FORM_GUIDELINES"))