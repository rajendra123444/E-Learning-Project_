from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Notes
    path('notes/', views.notes_list, name='notes_list'),
    path('notes/upload/', views.upload_note, name='upload_note'),
    path('notes/<int:note_id>/delete/', views.delete_note, name='delete_note'),
    path('notes/<int:note_id>/bookmark/', views.toggle_bookmark, name='toggle_bookmark'),
    path('notes/<int:note_id>/download/', views.download_note, name='download_note'),



    # Notes
    path('notes/', views.notes_list, name='notes_list'),
    path('notes/upload/', views.upload_note, name='upload_note'),
    path('notes/<int:note_id>/delete/', views.delete_note, name='delete_note'),
    path('notes/<int:note_id>/bookmark/', views.toggle_bookmark, name='toggle_bookmark'),
    path('notes/<int:note_id>/download/', views.download_note, name='download_note'),

    # User notes
    path('user/uploads/', views.my_uploads, name='my_uploads'),
    path('user/saved/', views.saved_notes, name='saved_notes'),

    # Books
    path('books/', views.books_list, name='books_list'),
    path('books/upload/', views.upload_book, name='upload_book'),

    # Syllabus / PYQs
    path('syllabus/', views.syllabus_list, name='syllabus_list'),
    path('syllabus/upload/', views.upload_syllabus, name='upload_syllabus'),


    path('pyqs/', views.pyqs_list, name='pyqs_list'),
    path('pyqs/upload/', views.upload_pyq, name='upload_pyq'),



    # Doubts
    path('doubts/', views.doubts_list, name='doubts_list'),
    path('doubts/ask/', views.ask_doubt, name='ask_doubt'),
    path('doubts/<int:doubt_id>/reply/', views.reply_to_doubt, name='reply_to_doubt'),
    path('replies/<int:reply_id>/mark_best/', views.mark_best_reply, name='mark_best_reply'),

    # Profile
    path('profile/', views.profile_data, name='profile_data'),
    path('profile/update/', views.update_profile, name='update_profile'),

    # Authentication (login, logout, register)

    #logout
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='/profile/'), name='logout'),  # no extra param

]

