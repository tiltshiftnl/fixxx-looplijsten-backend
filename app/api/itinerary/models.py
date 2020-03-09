from django.db import models
from api.users.models import User
from api.cases.models import Case, Project, State

class Itinerary(models.Model):
    """ Itinerary for visiting cases """
    created_at = models.DateField(auto_now_add=True)

    def clear_team_members(self):
        team_members = self.team_members.all()

        for team_member in team_members:
            team_member.delete()

    def add_team_members(self, user_ids):
        for user_id in user_ids:
            user = User.objects.get(id=user_id)
            ItineraryTeamMember.objects.create(user=user, itinerary=self)

    def __str__(self):
        team_members = self.team_members.all()
        team_members = [str(member) for member in team_members]
        string = ', '.join(team_members)

        return string

class ItinerarySettings(models.Model):
    opening_date = models.DateField(blank=False,
                                    null=False)

    target_itinerary_length = models.IntegerField(default=6)

    itinerary = models.OneToOneField(Itinerary,
                                     on_delete=models.CASCADE,
                                     null=False,
                                     unique=True,
                                     related_name='settings')

    projects = models.ManyToManyField(to=Project,
                                      blank=False,
                                      related_name='settings')

    primary_state = models.ForeignKey(to=State,
                                      on_delete=models.CASCADE,
                                      related_name='settings_as_primary_state')

    secondary_states = models.ManyToManyField(to=State,
                                              related_name='settings_as_secondary_state')

    exclude_states = models.ManyToManyField(to=State,
                                            related_name='settings_as_exclude_state')

    def __str__(self):
        return self.itinerary.__str__()


class ItineraryTeamMember(models.Model):

    class Meta:
        unique_together = ['user', 'itinerary']

    """ Member of an Itinerary Team """
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE, null=False,
                             related_name='teams',
                             related_query_name="user")

    itinerary = models.ForeignKey(Itinerary,
                                  on_delete=models.CASCADE,
                                  null=False,
                                  related_name='team_members')

    def __str__(self):
        return self.user.first_name

class ItineraryItem(models.Model):
    """ Single Itinerary """
    itinerary = models.ForeignKey(Itinerary, on_delete=models.CASCADE, null=False, related_name='items')
    case = models.ForeignKey(Case, on_delete=models.CASCADE, null=True, blank=False, related_name='cases')
    position = models.FloatField(null=False, blank=False)

    class Meta:
        ordering = ['position']

    def __str__(self):
        if self.case:
            return self.case.__str__()
        else:
            return ''

    def set_position_to_last(self):
        """ Sets this item's position to the last in the ItineraryItem list"""
        itinerary_item_list = self.itinerary.items.all().order_by('position')
        itinerary_items = list(itinerary_item_list)

        if(len(itinerary_items) == 0):
            self.position = 1
        else:
            last_item = itinerary_items[-1]
            self.position = last_item.position + 1

    def save(self, *args, **kwargs):
        # If no position is given, set the last the last in list
        if self.position is None:
            self.set_position_to_last()

        # Don't allow saving if another item in the list has the same position
        objects_with_same_position = self.itinerary.items.all().filter(position=self.position).exclude(pk=self.pk)

        if objects_with_same_position.exists():
            raise ValueError('An item with this position already exists')

        # Don't allow saving if the itinerary already contains the same case
        objects_with_same_case = self.itinerary.items.all().filter(case=self.case).exclude(pk=self.pk)

        if objects_with_same_case.exists():
            raise ValueError('The itinerary already contains this case')

        super().save(*args, **kwargs)

class Note(models.Model):
    """ A note for an Itinerary Item """
    itinerary_item = models.ForeignKey(ItineraryItem, on_delete=models.CASCADE,
                                       null=False, related_name='notes')
    text = models.TextField(null=False, blank=False)
    author = models.ForeignKey(to=User, null=True, blank=False, on_delete=models.CASCADE)

    def __str__(self):
        max_length = 20
        if len(self.text) > max_length:
            return '{}...'.format(self.text[:max_length])
        return self.text
