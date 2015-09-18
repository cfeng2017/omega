from apps.dao.dao_factory import GenericDAO


class GenericService(object):

    def __init__(self):
        super(GenericService, self).__init__()

    @classmethod
    def new(cls):
        return GenericDAO.new()

    @classmethod
    def find(cls):
        return GenericDAO.find()

    @classmethod
    def update(cls):
        return GenericDAO.update()

    @classmethod
    def delete(cls):
        return GenericDAO.delete()
