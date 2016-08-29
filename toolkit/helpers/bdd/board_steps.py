# from behave import *
#
# from bdd import fill_and_submit_form
#
#
#
# @step("I submit (valid|updated) (board|task) information")
# def create_profile(context, add_or_edit, target_variable):
#     b = context.browser
#
#     context.board_name = "Test Board"
#     context.board_description = "Test Description"
#     context.updated_board_name = "Updated Board Name"
#     context.task_title = "Test Task"
#     context.updated_task_title = "Updated Task Title"
#
#     if target_variable == "board":
#         if add_or_edit == "valid":
#
#             fields = [
#                 {'function': 'fill', 'name': 'name', 'value': context.board_name},
#                 {'function': 'fill', 'name': 'description', 'value': context.board_description},
#             ]
#
#             fill_and_submit_form(b, fields)
#
#         else:
#
#             fields = [
#                 {'function': 'fill', 'name': 'name', 'value': context.updated_board_name},
#             ]
#
#             fill_and_submit_form(b, fields)
#
#     else:
#         if add_or_edit == "valid":
#
#             fields = [
#                 {'function': 'fill', 'name': 'title', 'value': context.task_title},
#                 {'function': 'fill', 'name': 'image', 'value': '/home/local/CE/mwilcoxen/project/app/sample_app/storage/media/task_images/man.png'},
#                 {'function': 'select', 'name': 'board', 'value': 1},
#             ]
#
#             fill_and_submit_form(b, fields)
#
#         else:
#
#             fields = [
#                 {'function': 'fill', 'name': 'title', 'value': context.updated_task_title},
#             ]
#
#             fill_and_submit_form(b, fields)
#
#
# @step("I (should|shouldnt) see (the|the new|the updated) (board|task)")
# def check_for_object(context, should_or_shouldnt, add_or_edit, target_variable):
#     b = context.browser
#     expected_count = 1
#
#     if should_or_shouldnt == "should":
#         # add
#         if add_or_edit == "the new":
#
#             if target_variable == "board":
#                 assert Board.objects.filter(name=context.board_name).count() == expected_count
#                 assert b.is_text_present(context.board_name)
#
#             else:
#                 assert Task.objects.filter(title=context.task_title).count() == expected_count
#                 assert b.is_text_present(context.task_title)
#         # edit
#         elif add_or_edit == "the updated":
#
#             if target_variable == "board":
#                 assert Board.objects.filter(name=context.updated_board_name).count() == expected_count
#                 assert b.is_text_present(context.updated_board_name)
#
#             else:
#                 assert Task.objects.filter(title=context.updated_task_title).count() == expected_count
#                 assert b.is_text_present(context.updated_task_title)
#         # advanced search
#         else:
#             if target_variable == "board":
#                 assert b.is_text_present(context.board_name)
#
#             else:
#                 assert b.is_text_present(context.task_title)
#
#     if should_or_shouldnt == "shouldnt" and add_or_edit == "the":
#         # delete
#         if target_variable == "board":
#             assert Board.objects.filter(name=context.board_name).count() == 0
#
#         if target_variable == "task":
#             assert Task.objects.filter(title=context.task_title).count() == 0
#
#
# @step("I delete the (board|task)")
# def delete_things(context, board_or_task):
#     b = context.browser
#
#     b.find_by_name('submit').click()
#     assert b.is_text_present("No %ss found." % board_or_task)
#
#
# @step("I have a (board|task)")
# def create_things(context, board_or_task):
#     context.task_title = "Test Title"
#     context.task_description = "Test Task Description"
#     context.board_name = "Test Name"
#     context.board_description = "Test Board Description"
#
#     if board_or_task == "board":
#         context.test_board = Board.objects.create(name=context.board_name,
#                                                   description=context.board_description)
#     else:
#         context.test_task = Task.objects.create(title=context.task_title,
#                                                 description=context.task_description,
#                                                 image='/home/local/CE/mwilcoxen/project/app/sample_app/storage/media/task_images/man.png',
#                                                 board=context.test_board)
#
#
# @step("I use the (board|task|completed task) advanced search")
# def search_for_things(context, board_or_task):
#     b = context.browser
#     b.find_by_name('advanced_search_toggle').click()
#
#     if board_or_task == "board":
#         fields = [
#             {'function': 'fill', 'name': 'name', 'value': context.board_name},
#             {'function': 'fill', 'name': 'description', 'value': context.board_description},
#         ]
#
#         fill_and_submit_form(b, fields, 'advanced_search')
#
#         assert b.is_text_present(context.board_name)
#
#     else:
#         fields = [
#             {'function': 'fill', 'name': 'title', 'value': context.task_title},
#             {'function': 'fill', 'name': 'description', 'value': context.task_description},
#             {'function': 'select', 'name': 'boards', 'value': 1},
#         ]
#
#         fill_and_submit_form(b, fields, 'advanced_search')
#
#         assert b.is_text_present(context.task_title)
#
#
# @step("I click the (edit|delete) (board|task) button")
# def click_a_button(context, edit_or_delete, board_or_task):
#     b = context.browser
#
#     if board_or_task == "board":
#         b.find_link_by_partial_href("/b/1/%s" % edit_or_delete).click()
#
#     elif board_or_task == "task":
#         b.find_link_by_partial_href("/p/1/%s" % edit_or_delete).click()
