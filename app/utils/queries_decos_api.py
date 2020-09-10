class DecosJoinRequest:
    """
    Object to connect to decos join and retrieve permits
    """

    def get_checkmarks_with_bag_id(self, bag_id):
        response = {
            "has_b_and_b_permit": False,
            "has_vacation_rental_permit": True,
        }

        return response
