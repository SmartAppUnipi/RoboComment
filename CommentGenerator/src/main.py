from CommentMatcher import CommentMatcher
from CommentUpdater import CommentUpdater
from SentimentUpdater import SentimentUpdater


def main():
    # TODO capire come avviena la comunicazione tra i gruppi
    # se siamo noi a dover chidere in poll nuove azioni
    # se è il gruppo symbolic ad inviarci azioni
    # se è il gruppo audio a richiedere nuovi commenti <- ci piace

    cm = CommentMatcher()
    cu = CommentUpdater()
    su = SentimentUpdater()

    jsonobj = {}
    selected_comment = cm.pick_comment(jsonobj)
    updated_comment = cu.update_comment(selected_comment)
    final_output = su.add_emphasis(updated_comment)

    print(final_output)



main()