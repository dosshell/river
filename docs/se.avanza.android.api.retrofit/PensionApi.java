package se.avanza.android.api.retrofit;

import io.reactivex.Completable;
import io.reactivex.Single;
import retrofit2.t.a;
import retrofit2.t.e;
import retrofit2.t.m;
import retrofit2.t.q;
import se.avanza.android.api.domain.models.common.AccountId;
import se.avanza.android.api.models.pension.TjpFundDistribution;
import se.avanza.android.api.models.pension.TjpFundDistributionRequest;

/* compiled from: PensionApi.kt */
public interface PensionApi {
    @m("/_api/pension/tjp-fund-distribution/{accountId}")
    Completable createTjpFundDistribution(@q("accountId") AccountId accountId, @a TjpFundDistributionRequest tjpFundDistributionRequest);

    @e("/_mobile/pension/tjp-fund-distribution/{accountId}")
    Single<TjpFundDistribution> getTjpFundDistribution(@q("accountId") AccountId accountId);
}
