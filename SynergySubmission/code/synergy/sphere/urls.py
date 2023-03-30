from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.urls import reverse
from . import views
#all post/ urls are for event
# app_name = 'sphere'
# url = reverse('sphere:createcommunity')
urlpatterns = [
    path("", views.index, name="index"),
    path("n/login", views.login_view, name="login"),
    path("n/logout", views.logout_view, name="logout"),
    path("n/register", views.register, name="register"),
    # path("<str:username>", views.profile, name='profile'),
    path("n/following", views.following, name='following'),
    path("n/problems", views.problems, name='problems'),
    path("n/saved", views.saved, name="saved"),
    path("n/createpost", views.create_post, name="createpost"),
    path("n/postproblem",views.create_problem,name="createproblem"),
    path("n/createcommunity",views.create_org,name="createcommunity"),
    path("n/post/<int:id>/like", views.like_post, name="likepost"),
    path("n/post/<int:id>/unlike", views.unlike_post, name="unlikepost"),
    path("n/problem/<int:id>/like", views.like_problem, name="likeproblem"),
    path("n/problem/<int:id>/unlike", views.unlike_problem, name="unlikeproblem"),
    path("n/post/<int:id>/save", views.save_post, name="savepost"),
    path("n/post/<int:id>/unsave", views.unsave_post, name="unsavepost"),
    path("n/post/<int:event_id>/comments", views.event_comment, name="comments"),
    path("n/post/<int:event_id>/write_comment",views.event_comment, name="writecomment"),
    path("n/post/<int:event_id>/delete", views.delete_event, name="deletepost"),
    path("n/community/<int:org_id>/delete", views.delete_org, name="deleteorg"),
    path("n/problem/<int:problem_id>/comments", views.problem_comment, name="pcomments"),
    path("n/problem/<int:problem_id>/write_comment",views.problem_comment, name="writepcomment"),
    path("n/problem/<int:problem_id>/delete", views.delete_problem, name="deletepost"),
    path("<str:username>/follow", views.follow, name="followuser"),
    path("<str:username>/unfollow", views.unfollow, name="unfollowuser"),
    path("community/<int:org_id>/followcommunity", views.follow_org, name="followorg"),
    path("community/<int:org_id>/unfollowcommunity", views.unfollow_org, name="unfolloworg"),
    path("n/post/<int:post_id>/edit", views.edit_post, name="editpost"),
    path("n/problem/<int:post_id>/edit", views.edit_problem, name="editproblem"),
    path("<str:username>/communitylist", views.communitylist, name="communitylist"),
    path("<str:username>/createdcommunities", views.createdcommunities, name="createdcommunities"),
    path("<str:username>/followerlist", views.followerlist, name="followerlist"),
    path("<str:username>/followinglist", views.followinglist, name="followinglist"),
    path("n/post/<int:event_id>/e_likerlist", views.e_likerlist, name="e_likerlist"),
    path("n/problem<int:problem_id>/p_likerlist", views.p_likerlist, name="p_likerlist"),
    path("n/post/<int:event_id>/e_memberlist", views.e_memberlist, name="e_memberlist"),
    path("<str:org_name>", views.org_profile, name="org_profile"),
    path("<str:org_name>/memberlist", views.c_memberlist, name="c_memberlist"),
    # path("<str:username>/<int:org_id>", views.user, name="community"),
    path("<str:username>/community/<int:org_id>/createvent", views.communityevent, name="communityevent"),
    path("<str:username>/events", views.profile_events, name="profileevents"),
    path("<str:username>/problems", views.profile_problems, name="profileproblems"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
