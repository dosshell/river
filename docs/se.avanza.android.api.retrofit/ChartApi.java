package se.avanza.android.api.retrofit;

import io.reactivex.Single;
import retrofit2.t.e;
import retrofit2.t.j;
import retrofit2.t.q;
import retrofit2.t.r;
import se.avanza.android.api.domain.models.chart.ChartTimePeriod;
import se.avanza.android.api.domain.models.chart.ChartTimeResolution;
import se.avanza.android.api.domain.models.common.AccountId;
import se.avanza.android.api.domain.models.common.OrderbookId;
import se.avanza.android.api.models.chart.AccountChartResult;
import se.avanza.android.api.models.chart.OrderbookChartResult;

/* compiled from: ChartApi.kt */
public interface ChartApi {
    @e("/_mobile/chart/account/{accountId}")
    Single<AccountChartResult> getAccountChart(@q("accountId") AccountId accountId, @r("timePeriod") ChartTimePeriod chartTimePeriod, @r("resolution") ChartTimeResolution chartTimeResolution);

    @e("/_mobile/chart/{orderbookType}/{orderbookId}")
    Single<OrderbookChartResult> getChart(@q("orderbookId") OrderbookId orderbookId, @q("orderbookType") String str, @r("timePeriod") ChartTimePeriod chartTimePeriod, @r("resolution") ChartTimeResolution chartTimeResolution);

    @e("/_mobile/chart/{orderbookType}/{orderbookId}")
    @j({"AZA-Do-Not-Touch-Session: true"})
    Single<OrderbookChartResult> getChartWithoutRenewSession(@q("orderbookId") OrderbookId orderbookId, @q("orderbookType") String str, @r("timePeriod") ChartTimePeriod chartTimePeriod, @r("resolution") ChartTimeResolution chartTimeResolution);
}
