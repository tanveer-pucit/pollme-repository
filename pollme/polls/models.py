from django.contrib.auth.models import User
from django.db import models


class Poll(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    text = models.CharField(max_length=255)
    pub_date = models.DateField()

    def __str__(self):
        return self.text

    def user_can_vote(self, user):
        """Return False if user already voted else return True"""
        user_votes = user.vote_set.all()
        qs = user_votes.filter(poll=self)
        if qs.exists():
            return False
        return True

    @property
    def total_num_of_votes(self):
        return self.vote_set.count()

    def get_res_dect(self):
        """
        retuns a list of poll objects in the format given below
        [
            #for each related choices
            {
                'text': choice_text
                'total_num_of_votes': number of votes on that choice
                'percentage': chocie.total_num_of_votes_for_this_choice / poll.total_num_of_votes * 100
            }
        ]
        """
        result = []
        for choice in self.choice_set.all():
            dic = {}
            dic['text'] = choice.choice_text
            dic['total_votes'] = choice.total_num_of_votes_for_this_choice
            if not self.total_num_of_votes:
                dic['percentage'] = 0
            else:
                dic['percentage'] = choice.total_num_of_votes_for_this_choice / self.total_num_of_votes * 100
            result.append(dic)
        return result


class Choice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=255)

    def __str__(self):
        return "{} - {}".format(self.poll.text[:20], self.choice_text[:20])

    @property
    def total_num_of_votes_for_this_choice(self):
        return self.vote_set.count()


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
