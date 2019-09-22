package se.avanza.android.api.retrofit;

import io.reactivex.Completable;
import io.reactivex.Single;
import java.util.List;
import retrofit2.t.a;
import retrofit2.t.b;
import retrofit2.t.e;
import retrofit2.t.j;
import retrofit2.t.m;
import retrofit2.t.n;
import retrofit2.t.q;
import retrofit2.t.r;
import se.avanza.android.api.domain.models.common.OrderbookId;
import se.avanza.android.api.models.notifications.DeviceToken;
import se.avanza.android.api.models.notifications.NotificationSetting;
import se.avanza.android.api.models.notifications.PushSettingsRequest;
import se.avanza.android.api.models.notifications.PushSettingsResponse;
import se.avanza.android.api.models.notifications.pricealarm.OrderbookPriceAlertEntry;
import se.avanza.android.api.models.notifications.pricealarm.OrderbookPriceAlertRequest;
import se.avanza.android.api.models.notifications.pricealarm.PriceAlert;
import se.avanza.android.api.models.notifications.pricealarm.PriceAlertResponse;

/* compiled from: NotificationApi.kt */
public interface NotificationApi {
    @b("/_mobile/notification/unregister")
    Completable deleteDeviceToken(@r("googleDeviceToken") String str);

    @b("/_api/notification/pricealert/{alertId}")
    Completable deletePriceAlert(@q("alertId") String str);

    @e("/_mobile/notification/pricealerts/{orderbookId}")
    Single<List<PriceAlert>> getOrderbookPriceAlerts(@q("orderbookId") OrderbookId orderbookId);

    @e("/_mobile/notification/pricealert")
    Single<OrderbookPriceAlertEntry> loadOrderbookPriceAlert(@r("alertId") String str);

    @e("/_mobile/notification/pricealert")
    Single<OrderbookPriceAlertEntry> loadOrderbookPriceAlert(@r("orderbookId") OrderbookId orderbookId);

    @e("/_api/usercontent/notification-settings")
    Single<NotificationSetting> notificationSettings();

    @e("/_mobile/notification/pricealerts")
    Single<PriceAlertResponse> priceAlerts();

    @m("/_api/usercontent/notification-settings")
    Completable putNotificationSettings(@a NotificationSetting notificationSetting);

    @n("/_mobile/notification/settings")
    Completable putSettings(@a PushSettingsRequest pushSettingsRequest);

    @m("/_mobile/notification/register")
    @j({"AZA-Do-Not-Touch-Session: true"})
    Completable registerToken(@a DeviceToken deviceToken);

    @n("/_api/notification/pricealert")
    Completable saveOrderbookPriceAlert(@a OrderbookPriceAlertRequest orderbookPriceAlertRequest);

    @e("/_mobile/notification/settings")
    Single<PushSettingsResponse> settings();
}
