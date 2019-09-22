package se.avanza.android.api.retrofit;

import io.reactivex.Single;
import java.math.BigDecimal;
import java.util.List;
import retrofit2.t.e;
import retrofit2.t.q;
import retrofit2.t.r;
import se.avanza.android.api.domain.models.common.InspirationListId;
import se.avanza.android.api.domain.models.common.OrderbookId;
import se.avanza.android.api.models.discover.DocumentList;
import se.avanza.android.api.models.market.inspiration.InspirationList;
import se.avanza.android.api.models.market.inspiration.InspirationListOrderbook;
import se.avanza.android.api.models.marketing.autoportfolio.AutoPortfolio;
import se.avanza.android.api.models.marketing.autoportfolio.AutoPortfolioPrognosis;

/* compiled from: MarketingApi.kt */
public interface MarketingApi {
    @e("/_mobile/marketing/autoportfolio")
    Single<List<AutoPortfolio>> autoPortfolios();

    @e("/_mobile/marketing/autoportfolio/{orderbookId}")
    Single<AutoPortfolio> getAutoPortfolio(@q("orderbookId") OrderbookId orderbookId);

    @e("/_mobile/chart/autoportfolio/{orderbookId}/prognosis")
    Single<AutoPortfolioPrognosis> getAutoPrognosis(@q("orderbookId") OrderbookId orderbookId, @r("initialInvestment") BigDecimal bigDecimal, @r("monthlyInvestment") BigDecimal bigDecimal2);

    @e("/_mobile/content/document-list/{documentListId}")
    Single<DocumentList> getDocumentList(@q("documentListId") String str);

    @e("/_mobile/marketing/inspirationlist/{inspirationListId}")
    Single<InspirationList<InspirationListOrderbook>> getInspirationList(@q("inspirationListId") InspirationListId inspirationListId);

    @e("/_mobile/marketing/inspirationlist")
    Single<List<InspirationList<InspirationListOrderbook>>> inspirationLists();
}
