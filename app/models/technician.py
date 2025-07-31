# from utils.enums import ComplaintCategory
# import uuid

# class Technician:
#     def __init__(self, name, specializations):
#         self.id = str(uuid.uuid4())
#         self.name = name
#         self.specializations = specializations
#         self.is_available = True
#     def to_dict(self):
#         return {
#             'id': self.id,
#             'name': self.name,
#             'specializations': [spec.value for spec in self.specializations],
#             'is_available': self.is_available
#         }
#     # def make_unavailable(self):
#     #     return{
#     #         'id': ,
#     #         'name': self.name,
#     #         'specializations': [spec.value for spec in self.specializations],
#     #         'is_available': False
#     #     }