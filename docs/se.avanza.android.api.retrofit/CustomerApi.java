package se.avanza.android.api.retrofit;

import io.reactivex.Completable;
import io.reactivex.Maybe;
import io.reactivex.Single;
import retrofit2.t.e;
import retrofit2.t.n;
import retrofit2.t.r;
import se.avanza.android.api.domain.models.common.OrderbookId;
import se.avanza.android.api.models.customer.CustomerRegistration;
import se.avanza.android.api.models.customer.SignElegResponse;
import se.avanza.android.api.models.order.Suitability;
import se.avanza.android.core.authentication.IdentificationNumber;

/* compiled from: CustomerApi.kt */
public interface CustomerApi {
    @e("/_mobile/customer/check-suitability")
    Maybe<Suitability> checkSuitability(@r("orderbookId") OrderbookId orderbookId);

    @e("/_mobile/customer/registration/classify")
    Single<CustomerRegistration> customerRegistration();

    @e("/_mobile/customer/sign-eleg")
    Single<SignElegResponse> customerSigningDocument();

    @e("/_mobile/customer/registration/classify")
    Single<CustomerRegistration> getCustomerRegistration(@r("identificationNumber") IdentificationNumber identificationNumber);

    @e("/_mobile/customer/registration/are-all-accounts-active")
    Single<Boolean> registrationAccountsActiveStatus();

    @n("/_mobile/customer/prompts/swedish-citizenship-and-fiscal-residence/")
    Completable updateCustomerPrompt();
}
