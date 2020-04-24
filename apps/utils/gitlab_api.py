import gitlab

from restfuldemo.settings import GITLAB_HTTP_URI, GITLAB_TOKEN
gl = gitlab.Gitlab(GITLAB_HTTP_URI, GITLAB_TOKEN, api_version=4)

#
# def get_user_id(username):
#     """
#     通过用户名获取用户id
#     :param username:
#     :return:
#     """
#     user_lists = gl.users.list(all=True)
#     # print(user_lists)
#     for u in user_lists:
#         print('gitlab 用户是 ：%s' % u.name)
#         if u.name == username:
#             return u.id
#         else:
#             pass
#
#
# def get_user_projects(username):
#     """
#     获取用户所拥有的项目
#     :param userid:
#     :return:
#     """
#     print(username)
#     userid = get_user_id(username)
#     print(userid)
#     print(gl.projects.owned(userid=userid, all=True))
#     projects = gl.projects.owned(userid=userid, all=True)
#     return
    # result_list = []
    # for project in projects:
    #     result_list.append(project)
    # return result_list

def get_user_projects(username):
    """
    获取gitlab里所有的项目，和登录用户所拥有的项目,以及登录用户所拥有项目的项目成员
    :return: []
    """
    user_projects = []
    all_projects = gl.projects.list(all=True)
    print(len(all_projects))

    # 获取当前用户所有的项目
    for project in all_projects:
       # print(project)
        for member in project.members.list():
            # print(member)
            if member.username == username:
            # if member.username == "Sunfan":
                user_projects.append(project)
    return user_projects


def get_project_versions(project_id):
    """
    获取某个项目的版本号
    :param project_id:
    :return:
    """
    project = gl.projects.get(project_id)
    tags = project.tags.list()
    # print(tags)
    return tags

