package se.avanza.android.api.retrofit;

import io.reactivex.Observable;
import io.reactivex.Single;
import java.util.List;
import org.joda.time.DateTime;
import retrofit2.t.e;
import retrofit2.t.q;
import retrofit2.t.r;
import se.avanza.android.api.domain.models.common.AccountId;
import se.avanza.android.api.domain.models.common.OrderbookId;
import se.avanza.android.api.models.news.Article;
import se.avanza.android.api.models.news.Headline;
import se.avanza.android.api.models.news.HeadlineSection;

/* compiled from: NewsApi.kt */
public interface NewsApi {
    @e("/_mobile/news/account")
    Single<List<HeadlineSection>> getAccountHeadline();

    @e("/_mobile/news/account/{accountId}")
    Single<List<HeadlineSection>> getAccountHeadlines(@q("accountId") AccountId accountId);

    @e("/_mobile/news/article/{articlePath}")
    Observable<Article> getArticle(@q(encoded = true, value = "articlePath") String str);

    @e("/_mobile/news/headlines/{orderbookId}")
    Single<List<HeadlineSection>> getHeadlines(@q("orderbookId") OrderbookId orderbookId, @r("limit") int i2);

    @e("/_mobile/news/headlines/{orderbookIds}")
    Single<List<HeadlineSection>> getHeadlines(@q("orderbookIds") CommaSeparatedPath<OrderbookId> commaSeparatedPath);

    @e("/_mobile/news/newsbill")
    Single<List<Headline>> getNewsBill(@r("limit") int i2);

    @e("/_mobile/news/telegrams")
    Single<List<HeadlineSection>> getTelegrams(@r("limit") int i2);

    @e("/_mobile/news/telegrams")
    Single<List<HeadlineSection>> getTelegramsBefore(@r("timestamp") DateTime dateTime);
}
