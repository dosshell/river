package se.avanza.android.api.retrofit;

import io.reactivex.Completable;
import io.reactivex.Single;
import java.math.BigDecimal;
import retrofit2.t.a;
import retrofit2.t.b;
import retrofit2.t.e;
import retrofit2.t.m;
import retrofit2.t.n;
import retrofit2.t.q;
import retrofit2.t.r;
import se.avanza.android.api.domain.constants.InstrumentType;
import se.avanza.android.api.domain.constants.OrderType;
import se.avanza.android.api.domain.models.common.AccountId;
import se.avanza.android.api.domain.models.common.OrderId;
import se.avanza.android.api.domain.models.common.OrderbookId;
import se.avanza.android.api.models.order.InvestmentFees;
import se.avanza.android.api.models.order.OrderEntry;
import se.avanza.android.api.models.order.OrderEntryRequest;
import se.avanza.android.api.models.order.OrderEntryRequestResponse;
import se.avanza.android.api.models.order.TransactionFees;
import se.avanza.android.api.models.order.UpdateOrderEntryRequest;
import se.avanza.android.api.models.order.fund.FundOrderEntry;
import se.avanza.android.core.numbers.Volume;

/* compiled from: OrderApi.kt */
public interface OrderApi {

    /* compiled from: OrderApi.kt */
    public static final class DefaultImpls {
        @e("/_mobile/order/preliminary-investment-fees")
        public static /* synthetic */ Single getInvestmentFees$default(OrderApi orderApi, AccountId accountId, OrderbookId orderbookId, BigDecimal bigDecimal, Volume volume, Integer num, int i2, Object obj) {
            if (obj == null) {
                return orderApi.getInvestmentFees((i2 & 1) != 0 ? null : accountId, orderbookId, (i2 & 4) != 0 ? null : bigDecimal, (i2 & 8) != 0 ? null : volume, (i2 & 16) != 0 ? null : num);
            }
            throw new UnsupportedOperationException("Super calls with default arguments not supported in this target, function: getInvestmentFees");
        }
    }

    @b("/_api/order")
    Single<OrderEntryRequestResponse> deleteOrder(@r("accountId") AccountId accountId, @r("orderId") OrderId orderId);

    @e("/_mobile/order/preliminary-investment-fees")
    Single<InvestmentFees> getInvestmentFees(@r("accountId") AccountId accountId, @r("orderbookId") OrderbookId orderbookId, @r("price") BigDecimal bigDecimal, @r("volume") Volume volume, @r("yearsToHold") Integer num);

    @e("/_mobile/order/preliminary-transaction-fees")
    Single<TransactionFees> getTransactionFees(@r("accountId") AccountId accountId, @r("orderbookId") OrderbookId orderbookId, @r("orderId") OrderId orderId, @r("price") BigDecimal bigDecimal, @r("volume") Volume volume, @r("orderType") OrderType orderType);

    @e("/_mobile/order/fund")
    Single<FundOrderEntry> loadFundOrderInformation(@r("accountId") AccountId accountId, @r("orderbookId") OrderbookId orderbookId);

    @e("/_mobile/order")
    Single<OrderEntry> loadOrderInformation(@r("accountId") AccountId accountId, @r("orderbookId") OrderbookId orderbookId);

    @e("/_api/order")
    Single<OrderEntryRequestResponse> orderStatus(@r("accountId") AccountId accountId, @r("requestId") String str);

    @n("/_api/usercontent/settings/orderaccount/{accountId}")
    Completable saveOrderAccount(@q("accountId") AccountId accountId, @a String str);

    @m("/_api/usercontent/settings/showcourtageclassinfoonorderpage/{showCourtageDialog}")
    Completable saveShowCourtageInfoDialog(@q("showCourtageDialog") boolean z, @a String str);

    @m("/_api/order")
    Single<OrderEntryRequestResponse> sendOrder(@a OrderEntryRequest orderEntryRequest);

    @n("/_api/order/{instrumentType}/{orderId}")
    Single<OrderEntryRequestResponse> updateOrder(@q("instrumentType") InstrumentType instrumentType, @q("orderId") OrderId orderId, @a UpdateOrderEntryRequest updateOrderEntryRequest);
}
