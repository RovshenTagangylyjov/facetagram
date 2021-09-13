from django import template

register = template.Library()


@register.simple_tag()
def generate_room_id(user1_pk: int, user2_pk: int) -> int:
    users = sorted([user1_pk, user2_pk])
    return int('0'.join([str(users[0]), str(users[1])]))