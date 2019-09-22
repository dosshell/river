package se.avanza.android.api.retrofit;

import io.reactivex.Completable;
import io.reactivex.Single;
import retrofit2.t.a;
import retrofit2.t.b;
import retrofit2.t.e;
import retrofit2.t.m;
import retrofit2.t.n;
import retrofit2.t.q;
import se.avanza.android.api.domain.models.common.AccountId;
import se.avanza.android.api.domain.models.common.MonthlySavingsId;
import se.avanza.android.api.models.monthlysavings.MonthlySavingsRequest;
import se.avanza.android.api.models.monthlysavings.MonthlySavingsResponse;
import se.avanza.android.api.models.monthlysavings.MonthlySavingsSummary;
import se.avanza.android.api.models.transactions.MonthlySavingsDefaults;

/* compiled from: MonthlySavingsApi.kt */
public interface MonthlySavingsApi {
    @m("/_api/transfer/monthly-savings/{accountId}")
    Single<MonthlySavingsResponse> createMonthlySavings(@q("accountId") AccountId accountId, @a MonthlySavingsRequest monthlySavingsRequest);

    @e("/_mobile/transfer/monthly-savings/{accountId}")
    Single<MonthlySavingsSummary> getMonthlySavings(@q("accountId") AccountId accountId);

    @e("/_mobile/transfer/monthly-savings")
    Single<MonthlySavingsSummary> monthlySavings();

    @e("/_mobile/transfer/monthly-savings-defaults")
    Single<MonthlySavingsDefaults> monthlySavingsDefaults();

    @n("/_api/transfer/monthly-savings/{accountId}/{monthlySavingsId}/pause")
    Completable pauseMonthlySavings(@q("accountId") AccountId accountId, @q("monthlySavingsId") MonthlySavingsId monthlySavingsId);

    @b("/_api/transfer/monthly-savings/{accountId}/{monthlySavingsId}")
    Completable removeMonthlySavings(@q("accountId") AccountId accountId, @q("monthlySavingsId") MonthlySavingsId monthlySavingsId);

    @n("/_api/transfer/monthly-savings/{accountId}/{monthlySavingsId}/resume")
    Completable resumeMonthlySavings(@q("accountId") AccountId accountId, @q("monthlySavingsId") MonthlySavingsId monthlySavingsId);
}
