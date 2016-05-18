import database

def requirements_met(OSIS):
    """
    requirements_met: returns a list containing dict objects of the various graduation requirements.

    Args:
    OSIS (string): 9 digit id of student to check
    Returns:
    List of dicts of grade requirements and progress thus far
    ex: [
        {
          "name": "Art Appreciation",
          "completed" : True,
          "progress" : [
            {
             "track_name":"Art Appreciation",
             "terms-req" : 1,
             "terms-passed" : 1,
             "course-codes" : ["AHS11"]
            }
          ]
        },
        {
        "name": "Music Appreciation",
          "completed" : False,
          "progress" : [
            {
             "track_name":"3 Terms Chorus",
             "terms-req" : 3,
             "terms-passed" : 1,
             "course-codes" : ["UVS11"]
            }
          ]
        },
        ]
