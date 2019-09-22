package se.avanza.android.api.retrofit;

import io.reactivex.Completable;
import io.reactivex.Single;
import java.util.List;
import java.util.Map;
import retrofit2.t.a;
import retrofit2.t.b;
import retrofit2.t.e;
import retrofit2.t.i;
import retrofit2.t.m;
import retrofit2.t.n;
import retrofit2.t.q;
import se.avanza.android.api.models.watchlist.WatchList;

/* compiled from: WatchListApi.kt */
public interface WatchListApi {
    @m("/_api/usercontent/watchlist")
    Single<String> add(@a WatchList watchList);

    @b("/_api/usercontent/watchlist/{watchListId}")
    Completable remove(@q("watchListId") String str);

    @n("/_api/usercontent/watchlist/{watchListId}")
    Completable update(@q("watchListId") String str, @a WatchList watchList);

    @e("/_mobile/usercontent/watchlist")
    Single<List<WatchList>> watchlists(@i Map<String, String> map);
}
