"""Provides routing to all submodules inside the application
"""
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings as django_settings
from django.contrib.auth import views as auth_views

from .forms.authentication import PasswordResetConfirmForm
from .views import (
    accommodations,
    authentication,
    analytics,
    bed_target_groups,
    dashboard,
    events,
    offers,
    offer_templates,
    language_tree,
    languages,
    media,
    organizations,
    pages,
    pois,
    push_notifications,
    regions,
    requests,
    roles,
    settings,
    statistics,
    users
)


urlpatterns = [
    url(r'^$', dashboard.RedirectView.as_view(), name='redirect'),
    url(r'^admin_dashboard/$', dashboard.AdminDashboardView.as_view(), name='admin_dashboard'),
    url(r'^regions/', include([
        url(r'^$', regions.RegionListView.as_view(), name='regions'),
        url(r'^new$', regions.RegionView.as_view(), name='new_region'),
        url(r'^(?P<region_slug>[-\w]+)/', include([
            url(
                r'^edit$',
                regions.RegionView.as_view(),
                name='edit_region'
            ),
            url(
                r'^delete$',
                regions.delete_region,
                name='delete_region'
            ),
        ])),
    ])),
    url(r'^languages/', include([
        url(r'^$', languages.LanguageListView.as_view(), name='languages'),
        url(r'^new$', languages.LanguageView.as_view(), name='new_language'),
        url(r'^(?P<language_code>[-\w]+)/', include([
            url(
                r'^edit$',
                languages.LanguageView.as_view(),
                name='edit_language'
            ),
            url(
                r'^delete$',
                languages.LanguageView.as_view(),
                name='delete_language'
            ),
        ])),
    ])),
    url(r'^users/', include([
        url(r'^$', users.UserListView.as_view(), name='users'),
        url(r'^new$', users.UserView.as_view(), name='new_user'),
        url(r'^(?P<user_id>[0-9]+)/', include([
            url(
                r'^edit$',
                users.UserView.as_view(),
                name='edit_user'
            ),
            url(
                r'^delete$',
                users.delete_user,
                name='delete_user'
            ),
        ])),
    ])),
    url(r'^roles/', include([
        url(r'^$', roles.RoleListView.as_view(), name='roles'),
        url(r'^new$', roles.RoleView.as_view(), name='new_role'),
        url(r'^(?P<role_id>[0-9]+)/', include([
            url(
                r'^edit$',
                roles.RoleView.as_view(),
                name='edit_role'
            ),
            url(
                r'^delete$',
                roles.RoleView.as_view(),
                name='delete_role'
            ),
        ])),
    ])),
    url(r'^organizations/', include([
        url(r'^$', organizations.OrganizationListView.as_view(), name='organizations'),
        url(r'^new$', organizations.OrganizationView.as_view(), name='new_organization'),
        url(r'^(?P<organization_id>[0-9]+)/', include([
            url(
                r'^edit$',
                organizations.OrganizationView.as_view(),
                name='edit_organization'
            ),
            url(
                r'^delete$',
                organizations.OrganizationView.as_view(),
                name='delete_organization'
            ),
        ])),
    ])),
    url(r'^bed_target_groups/', include([
        url(r'^$', bed_target_groups.BedTargetGroupListView.as_view(), name='bed_target_groups'),
        url(r'^new$', bed_target_groups.BedTargetGroupView.as_view(), name='new_bed_target_group'),
        url(r'^(?P<bed_target_group_id>[0-9]+)/', include([
            url(
                r'^edit$',
                bed_target_groups.BedTargetGroupView.as_view(),
                name='edit_bed_target_group'
            ),
            url(
                r'^delete$',
                bed_target_groups.delete_bed_target_group,
                name='delete_bed_target_group'
            ),
        ])),
    ])),
    url(r'^offer_templates/', include([
        url(r'^$', offer_templates.OfferTemplateListView.as_view(), name='offer_templates'),
        url(r'^new$', offer_templates.OfferTemplateView.as_view(), name='new_offer_template'),
        url(r'^(?P<offer_template_id>[0-9]+)/', include([
            url(
                r'^edit$',
                offer_templates.OfferTemplateView.as_view(),
                name='edit_offer_template'
            ),
            url(
                r'^delete$',
                offer_templates.OfferTemplateView.as_view(),
                name='delete_offer_templates'
            ),
        ])),
    ])),

    url(r'^settings/$', settings.AdminSettingsView.as_view(), name='admin_settings'),
    url(r'^user_settings/$', settings.UserSettingsView.as_view(), name='user_settings'),
    url(r'^user_settings/mfa/register/$', settings.mfa.register_mfa_key, name='user_settings_register_mfa_key'),
    url(r'^user_settings/mfa/delete/(?P<key_id>\d+)$', settings.mfa.DeleteMfaKey.as_view(), name='user_settings_delete_mfa_key'),
    url(r'^user_settings/mfa/get_challenge/$', settings.mfa.GetChallengeView.as_view(), name='user_settings_mfa_get_challenge'),
    url(r'^user_settings/add_new_mfa_key/$', settings.mfa.AddMfaKeyView.as_view(), name='user_settings_add_new_mfa_key'),
    url(r'^user_settings/authenticate_modify_mfa/$', settings.mfa.AuthenticateModifyMfaView.as_view(), name='user_settings_auth_modify_mfa'),
    url(r'^login/$', authentication.login, name='login'),
    url(r'^login/mfa/$', authentication.mfa, name='login_mfa'),
    url(r'^login/mfa/assert$', authentication.mfaAssert, name='login_mfa_assert'),
    url(r'^login/mfa/verify$', authentication.mfaVerify, name='login_mfa_verify'),
    url(r'^logout/$', authentication.logout, name='logout'),
    url(r'^password_reset/', include([
        url(
            r'$',
            auth_views.PasswordResetView.as_view(),
            name='password_reset'
        ),
        url(
            r'^done/$',
            authentication.password_reset_done,
            name='password_reset_done'
        ),
        url(
            r'^(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
            auth_views.PasswordResetConfirmView.as_view(form_class=PasswordResetConfirmForm),
            name='password_reset_confirm'
        ),
        url(
            r'^complete/$',
            authentication.password_reset_complete,
            name='password_reset_complete'
        ),
    ])),

    url(r'^ajax/', include([
        url(
            r'^grant_page_permission$',
            pages.grant_page_permission_ajax,
            name='grant_page_permission_ajax'
        ),
        url(
            r'^revoke_page_permission$',
            pages.revoke_page_permission_ajax,
            name='revoke_page_permission_ajax'
        ),
        url(
            r'^get_pages_list$',
            pages.get_pages_list_ajax,
            name='get_pages_list_ajax'
        ),
        url(
            r'^save_mirrored_page$',
            pages.save_mirrored_page,
            name='save_mirrored_page'
        ),
        url(
            r'^search_poi$',
            events.search_poi_ajax,
            name='search_poi_ajax'
        ),
    ])),

    url(r'^(?P<region_slug>[-\w]+)/', include([
        url(r'^$', dashboard.DashboardView.as_view(), name='dashboard'),
        url(r'^translation_coverage/', analytics.TranslationCoverageView.as_view(), name='translation_coverage'),
        url(r'^pages/', include([
            url(r'^$', pages.PageTreeView.as_view(), name='pages'),
            url(r'^(?P<language_code>[-\w]+)/', include([
                url(r'^$', pages.PageTreeView.as_view(), name='pages'),
                url(r'^new$', pages.PageView.as_view(), name='new_page'),
                url(r'^archived$', pages.PageTreeView.as_view(archived=True), name='archived_pages'),
                url(r'^upload$', pages.upload_page, name='upload_page'),
                url(r'^(?P<page_id>[0-9]+)/', include([
                    url(
                        r'^view$',
                        pages.view_page,
                        name='view_page'
                    ),
                    url(
                        r'^edit$',
                        pages.PageView.as_view(),
                        name='edit_page'
                    ),
                    url(
                        r'^sbs_edit$',
                        pages.PageSideBySideView.as_view(),
                        name='sbs_edit_page'
                    ),
                    url(
                        r'^archive$',
                        pages.archive_page,
                        name='archive_page'
                    ),
                    url(
                        r'^restore$',
                        pages.restore_page,
                        name='restore_page'
                    ),
                    url(
                        r'^delete$',
                        pages.delete_page,
                        name='delete_page'
                    ),
                    url(
                        r'^download$',
                        pages.download_page_xliff,
                        name='download_page'
                    ),
                    # warning: the move url is also hardcoded in the javascript block of backend/cms/templates/pages/tree.html
                    url(
                        r'^move/(?P<target_id>[0-9]+)/(?P<position>[-\w]+)$',
                        pages.move_page,
                        name='move_page'
                    ),
                ])),
            ])),
        ])),
        # TODO: Change destination for delete_event, add view_event
        url(r'^events/', include([
            url(r'^$', events.EventListView.as_view(), name='events'),
            url(r'^(?P<language_code>[-\w]+)/', include([
                url(r'^$', events.EventListView.as_view(), name='events'),
                url(r'^archived$', events.EventListView.as_view(archived=True), name='events_archived'),
                url(r'^new$', events.EventView.as_view(), name='new_event'),
                url(r'^(?P<event_id>[0-9]+)/', include([
                    url(r'^edit$', events.EventView.as_view(), name='edit_event'),
                    url(r'^archive$', events.archive, name='archive_event'),
                    url(r'^restore$', events.restore, name='restore_event'),
                    url(r'^delete$', events.delete, name='delete_event'),
                ])),
            ])),
        ])),
        url(r'^requests/', include([
            url(r'^$', requests.RequestListView.as_view(), name='requests'),
            url(r'^archived$', requests.RequestListView.as_view(archived=True), name='archived_requests'),
            url(r'^new$', requests.RequestView.as_view(), name='new_request'),
            url(r'^(?P<request_id>[0-9]+)/', include([
                url(r'^view$', requests.view_request, name='view_request'),
                url(r'^edit$', requests.RequestView.as_view(), name='edit_request'),
                url(r'^archive$', requests.archive_request, name='archive_request'),
                url(r'^restore$', requests.restore_request, name='restore_request'),
                url(r'^delete$', requests.delete_request, name='delete_request'),
            ])),
        ])),
        url(r'^pois/', include([
            url(r'^$', pois.POIListView.as_view(), name='pois'),
            url(r'^(?P<language_code>[-\w]+)/', include([
                url(r'^$', pois.POIListView.as_view(), name='pois'),
                url(r'^archived$', pois.POIListView.as_view(archived=True), name='archived_pois'),
                url(r'^new$', pois.POIView.as_view(), name='new_poi'),
                url(r'^(?P<poi_id>[0-9]+)/', include([
                    url(r'^view$', pois.view_poi, name='view_poi'),
                    url(r'^edit$', pois.POIView.as_view(), name='edit_poi'),
                    url(r'^archive$', pois.archive_poi, name='archive_poi'),
                    url(r'^restore$', pois.restore_poi, name='restore_poi'),
                    url(r'^delete$', pois.delete_poi, name='delete_poi'),
                ])),
            ])),
        ])),
        url(r'^accommodations/', include([
            url(r'^$', accommodations.AccommodationListView.as_view(), name='accommodations'),
            url(r'^(?P<language_code>[-\w]+)/', include([
                url(r'^$', accommodations.AccommodationListView.as_view(), name='accommodations'),
                url(r'^archived$', accommodations.AccommodationListView.as_view(archived=True), name='archived_accommodations'),
                url(r'^new$', accommodations.AccommodationView.as_view(), name='new_accommodation'),
                url(r'^(?P<accommodation_id>[0-9]+)/', include([
                    url(r'^view$', accommodations.view_accommodation, name='view_accommodation'),
                    url(r'^edit$', accommodations.AccommodationView.as_view(), name='edit_accommodation'),
                    url(r'^archive$', accommodations.archive_accommodation, name='archive_accommodation'),
                    url(r'^restore$', accommodations.restore_accommodation, name='restore_accommodation'),
                    url(r'^delete$', accommodations.delete_accommodation, name='delete_accommodation'),
                    url(r'^beds', accommodations.BedsView.as_view(), name='manage_beds')
                ])),
            ])),
        ])),
        url(r'^push_notifications/', include([
            url(r'^$', push_notifications.PushNotificationListView.as_view(), name='push_notifications'),
            url(r'^(?P<language_code>[-\w]+)/', include([
                url(r'^$', push_notifications.PushNotificationListView.as_view(), name='push_notifications'),
                url(r'^new$', push_notifications.PushNotificationView.as_view(), name='new_push_notification'),
                url(r'^(?P<push_notification_id>[0-9]+)/', include([
                    url(
                        r'^edit$',
                        push_notifications.PushNotificationView.as_view(),
                        name='edit_push_notification'
                    ),
                ])),
            ])),
        ])),
        url(r'^offers/', include([
            url(r'^$', offers.OfferListView.as_view(), name='offers'),
            url(r'^(?P<offer_template_slug>[-\w]+)/', include([
                url(
                    r'^activate$',
                    offers.activate,
                    name='activate_offer'
                ),
                url(
                    r'^deactivate$',
                    offers.deactivate,
                    name='deactivate_offer'
                ),
            ])),
        ])),
        url(r'^language-tree/', include([
            url(r'^$', language_tree.LanguageTreeView.as_view(), name='language_tree'),
            url(
                r'^new$',
                language_tree.LanguageTreeNodeView.as_view(),
                name='new_language_tree_node'
            ),
            url(r'^(?P<language_tree_node_id>[0-9]+)/', include([
                url(
                    r'^edit$',
                    language_tree.LanguageTreeNodeView.as_view(),
                    name='edit_language_tree_node'
                ),
                url(
                    r'^delete$',
                    language_tree.LanguageTreeNodeView.as_view(),
                    name='delete_language_tree_node'
                ),
            ])),
        ])),
        url(r'^statistics/$', statistics.AnalyticsView.as_view(), name='statistics'),
        url(r'^settings/$', settings.SettingsView.as_view(), name='settings'),
        url(r'^media/', include([
            url(r'^$', media.MediaListView.as_view(), name='media'),
            url(r'^(?P<document_id>[0-9]+)/', include([
                url(r'^new$', media.MediaEditView.as_view(), name='new_upload_file'),
                url(r'^edit$', media.MediaEditView.as_view(), name='edit_file'),
                url(r'^delete$', media.delete_file, name='delete_file'),
            ])),
        ])),
        url(r'^users/', include([
            url(r'^$', users.RegionUserListView.as_view(), name='region_users'),
            url(r'^new$', users.RegionUserView.as_view(), name='new_region_user'),
            url(r'^(?P<user_id>[0-9]+)/', include([
                url(
                    r'^edit$',
                    users.RegionUserView.as_view(),
                    name='edit_region_user'
                ),
                url(
                    r'^delete$',
                    users.delete_region_user,
                    name='delete_region_user'
                ),
            ])),
        ])),
    ])),
] + static(django_settings.MEDIA_URL, document_root=django_settings.MEDIA_ROOT)
