package se.avanza.android.api.retrofit;

import io.reactivex.Single;
import retrofit2.t.e;
import retrofit2.t.q;
import se.avanza.android.api.models.external.mortage.ExternalMortgage;
import se.avanza.android.api.models.external.mortage.ExternalMortgageApplicationId;
import se.avanza.android.api.models.external.mortage.ExternalMortgageList;

/* compiled from: ExternalMortgageApi.kt */
public interface ExternalMortgageApi {
    @e("/_mobile/external-mortgage/list")
    Single<ExternalMortgageList> externalMortgages();

    @e("/_mobile/external-mortgage/{id}/overview")
    Single<ExternalMortgage> getExternalMortgage(@q("id") ExternalMortgageApplicationId externalMortgageApplicationId);
}
