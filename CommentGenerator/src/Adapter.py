class Adapter:
    def __init__(self):
        self.structure = {
            "user_id": -1,
            "time": {"start": -1,
                     "end": -1
                     },
            "type": "elementary",
            "details":[]
        }

    def adapt(self, jsonobj):
        for x, y in jsonobj.items():
            print(x, y)


if __name__ == '__main__':
    adapter = Adapter()


    with open("CommentGenerator/assets/input1.json", 'r') as input1_json:
        input_json = json.load(input1_json)
        # TODO add test test and test
        print("INPUT:", input_json)
        comment = adapter.adapt(input_json)
        print("\nFINAL comment:", comment)

    # TODO idea, use a model to rephrase the comment to obtain human readable and grammar spell checks
    # check python paraphrase sentence and evaluate if split correction to paraphrase