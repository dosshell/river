package se.avanza.android.api.retrofit;

import io.reactivex.Maybe;
import io.reactivex.Single;
import java.util.List;
import retrofit2.t.e;
import retrofit2.t.j;
import retrofit2.t.r;
import se.avanza.android.api.models.system.AndroidOsVersion;
import se.avanza.android.api.models.system.MobileAppVersion;
import se.avanza.android.api.models.system.OpeningHours;
import se.avanza.android.api.models.system.RoutingUrlItem;
import se.avanza.android.api.models.system.SystemMessage;

/* compiled from: SystemApi.kt */
public interface SystemApi {
    @e("/_mobile/system/check-version/android")
    @j({"AZA-Do-Not-Touch-Session: true"})
    Maybe<MobileAppVersion> checkVersion(@r("currentVersion") String str, @r("currentOSVersion") AndroidOsVersion androidOsVersion);

    @e("/systemmeddelanden/mobil/global")
    @j({"AZA-Do-Not-Touch-Session: true", "Content-Type: text/plain"})
    Single<String> fallbackSystemMessage();

    @e("/_mobile/system/features/android")
    @j({"AZA-Do-Not-Touch-Session: true"})
    Single<List<String>> featureToggles();

    @e("/_mobile/system/customer-service/opening-hours")
    Single<List<OpeningHours>> openingHours();

    @e("/_mobile/system/messages")
    @j({"AZA-Do-Not-Touch-Session: true"})
    Single<List<SystemMessage>> systemMessages();

    @e("/_mobile/system/urlmappings")
    @j({"AZA-Do-Not-Touch-Session: true"})
    Single<List<RoutingUrlItem>> urlLinkTable();
}
