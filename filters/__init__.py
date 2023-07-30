from loader import dp
from .admins import AdminFilter
from .group_filter import GroupFilter
from .private_filter import Private



if __name__ == "filters":
    dp.filters_factory.bind(AdminFilter)
    dp.filters_factory.bind(Private)
    dp.filters_factory.bind(GroupFilter)
