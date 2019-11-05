#from xml.dom import minidom

# "<comment> <subject> Cristiano Ronaldo </subject> has made a pass </comment>"
template_dictionary = {
    "pass" : [
        "Cristiano Ronaldo has made a pass"
    ]
}



class CommentMatcher():

    def pick_comment(self, input_json):
        ''' it gets a json object in input '''

        return template_dictionary["pass"][0]
