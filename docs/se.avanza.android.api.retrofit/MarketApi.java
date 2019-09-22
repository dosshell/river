package se.avanza.android.api.retrofit;

import io.reactivex.Single;
import java.util.List;
import retrofit2.t.e;
import retrofit2.t.j;
import retrofit2.t.q;
import retrofit2.t.r;
import se.avanza.android.api.common.OrderbookSortOrder;
import se.avanza.android.api.domain.constants.InstrumentType;
import se.avanza.android.api.domain.models.common.OrderbookId;
import se.avanza.android.api.models.market.SelectableIndex;
import se.avanza.android.api.models.market.orderbook.Bond;
import se.avanza.android.api.models.market.orderbook.Certificate;
import se.avanza.android.api.models.market.orderbook.ExchangeTradedFund;
import se.avanza.android.api.models.market.orderbook.Fund;
import se.avanza.android.api.models.market.orderbook.FutureForward;
import se.avanza.android.api.models.market.orderbook.Index;
import se.avanza.android.api.models.market.orderbook.Option;
import se.avanza.android.api.models.market.orderbook.Stock;
import se.avanza.android.api.models.market.orderbook.Warrant;
import se.avanza.android.api.models.market.overview.AbstractMarketOrderbook;
import se.avanza.android.api.models.market.overview.MarketOrderbookGroup;
import se.avanza.android.api.models.market.overview.MarketOverviewGroup;
import se.avanza.android.api.models.market.search.SearchResult;

/* compiled from: MarketApi.kt */
public interface MarketApi {
    @e("/_mobile/market/bond/{orderbookId}")
    Single<Bond> getBond(@q("orderbookId") OrderbookId orderbookId);

    @e("/_mobile/market/certificate/{orderbookId}")
    Single<Certificate> getCertificate(@q("orderbookId") OrderbookId orderbookId);

    @e("/_mobile/market/orderbooklist/{orderbookIds}?group=none&sort=none")
    Single<List<AbstractMarketOrderbook>> getCustomSortedOrderbooks(@q("orderbookIds") CommaSeparatedPath<OrderbookId> commaSeparatedPath);

    @e("/_mobile/market/equity_linked_bond/{orderbookId}")
    Single<Bond> getEquityLinkedBond(@q("orderbookId") OrderbookId orderbookId);

    @e("/_mobile/market/exchange_traded_fund/{orderbookId}")
    Single<ExchangeTradedFund> getExchangeTradedFund(@q("orderbookId") OrderbookId orderbookId);

    @e("/_mobile/market/fund/{orderbookId}")
    Single<Fund> getFund(@q("orderbookId") OrderbookId orderbookId);

    @e("/_mobile/market/future_forward/{orderbookId}")
    Single<FutureForward> getFutureForward(@q("orderbookId") OrderbookId orderbookId);

    @e("/_mobile/market/index/{orderbookId}")
    Single<Index> getIndex(@q("orderbookId") OrderbookId orderbookId);

    @e("/_mobile/market/option/{orderbookId}")
    Single<Option> getOption(@q("orderbookId") OrderbookId orderbookId);

    @e("/_mobile/market/orderbooklist/{orderbookIds}?group=type")
    Single<List<MarketOrderbookGroup>> getSortedOrderbooks(@q("orderbookIds") CommaSeparatedPath<OrderbookId> commaSeparatedPath, @r("sort") OrderbookSortOrder orderbookSortOrder);

    @e("/_mobile/market/orderbooklist/{orderbookIds}?group=type")
    @j({"AZA-Do-Not-Touch-Session: true"})
    Single<List<MarketOrderbookGroup>> getSortedOrderbooksNoTouchSession(@q("orderbookIds") CommaSeparatedPath<OrderbookId> commaSeparatedPath, @r("sort") OrderbookSortOrder orderbookSortOrder);

    @e("/_mobile/market/stock/{orderbookId}")
    Single<Stock> getStock(@q("orderbookId") OrderbookId orderbookId);

    @e("/_mobile/market/warrant/{orderbookId}")
    Single<Warrant> getWarrant(@q("orderbookId") OrderbookId orderbookId);

    @e("/_mobile/market/overview")
    Single<List<MarketOverviewGroup>> marketIndices();

    @e("/_mobile/market/search")
    Single<SearchResult> search(@r("query") String str, @r("limit") int i2, @r("onlyBuyable") boolean z);

    @e("/_mobile/market/search/{instrumentType}")
    Single<SearchResult> search(@q("instrumentType") InstrumentType instrumentType, @r("query") String str, @r("limit") int i2, @r("onlyBuyable") boolean z);

    @e("/_mobile/market/selectableindex")
    Single<List<SelectableIndex>> selectableIndices();
}
