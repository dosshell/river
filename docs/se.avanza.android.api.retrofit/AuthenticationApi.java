package se.avanza.android.api.retrofit;

import io.reactivex.Completable;
import io.reactivex.Single;
import retrofit2.t.a;
import retrofit2.t.b;
import retrofit2.t.e;
import retrofit2.t.h;
import retrofit2.t.m;
import retrofit2.t.q;
import retrofit2.t.r;
import se.avanza.android.api.models.biometrics.ActivateDeviceTokenRequest;
import se.avanza.android.api.models.biometrics.EnableDeviceTokenRequest;
import se.avanza.android.api.models.biometrics.EnableDeviceTokenResponse;
import se.avanza.android.api.models.biometrics.LoginDeviceTokenRequest;
import se.avanza.android.api.models.biometrics.SendActivationCodeResponse;
import se.avanza.android.api.models.biometrics.VerifyActivationCodeRequest;
import se.avanza.android.api.models.biometrics.VerifyActivationCodeResponse;
import se.avanza.android.api.models.login.BankIdAuthentication;
import se.avanza.android.api.models.login.BankIdCollectionState;
import se.avanza.android.api.models.login.BankIdTransaction;
import se.avanza.android.api.models.login.RecoverPasswordRequest;
import se.avanza.android.api.models.login.RecoverUsernameRequest;
import se.avanza.android.api.models.login.TotpAuthentication;
import se.avanza.android.api.models.login.TwoFactorAuthenticationResponse;
import se.avanza.android.api.models.login.UserLogin;
import se.avanza.android.api.models.login.UserSession;
import se.avanza.android.api.models.totp.TotpVerify;
import se.avanza.android.api.models.totp.TwofactorTransactionId;
import se.avanza.android.core.authentication.IdentificationNumber;

/* compiled from: AuthenticationApi.kt */
public interface AuthenticationApi {
    public static final Companion Companion = Companion.$$INSTANCE;
    public static final String HEADER_TOTP_TRANSACTION_ID = "VND.se.avanza.security-Totp-Transaction-Id";
    public static final String HEADER_TWOFACTOR_TRANSACTION_ID = "VND.se.avanza.security-TwoFactor-Activation-Transaction-Id";

    /* compiled from: AuthenticationApi.kt */
    public static final class Companion {
        static final /* synthetic */ Companion $$INSTANCE = new Companion();
        public static final String HEADER_TOTP_TRANSACTION_ID = "VND.se.avanza.security-Totp-Transaction-Id";
        public static final String HEADER_TWOFACTOR_TRANSACTION_ID = "VND.se.avanza.security-TwoFactor-Activation-Transaction-Id";

        private Companion() {
        }
    }

    @m("/_api/authentication/enabledevicetoken/activate-devicetoken")
    Single<UserSession> activateDeviceToken(@a ActivateDeviceTokenRequest activateDeviceTokenRequest, @h("VND.se.avanza.security-TwoFactor-Activation-Transaction-Id") String str);

    @m("/_api/authentication/sessions/bankid")
    Single<BankIdTransaction> authenticate();

    @m("/_api/authentication/sessions/usercredentials")
    Single<TwoFactorAuthenticationResponse> authenticate(@a UserLogin userLogin);

    @m("/_api/authentication/sessions/bankid")
    Single<BankIdTransaction> authenticate(@a IdentificationNumber identificationNumber);

    @e("{authURL}")
    Single<BankIdAuthentication> authenticateAccount(@q(encoded = true, value = "authURL") String str, @r("maxInactiveMinutes") int i2);

    @e("/_api/authentication/sessions/bankid/{transactionId}")
    Single<BankIdCollectionState> collect(@q("transactionId") String str);

    @m("/_api/authentication/enabledevicetoken")
    Single<EnableDeviceTokenResponse> enableDeviceToken(@a EnableDeviceTokenRequest enableDeviceTokenRequest);

    @m("/_api/authentication/sessions/devicetoken")
    Single<UserSession> loginDeviceToken(@a LoginDeviceTokenRequest loginDeviceTokenRequest);

    @b("/_api/authentication/sessions/{sessionId}")
    Completable logout(@q("sessionId") String str);

    @m("/_api/authentication/usercredentials/request-new-password")
    Completable recoverPassword(@a RecoverPasswordRequest recoverPasswordRequest);

    @m("/_api/authentication/usercredentials/recover-username")
    Completable recoverUsername(@a RecoverUsernameRequest recoverUsernameRequest);

    @m("/_api/authentication/enabledevicetoken/send-activationcode")
    Single<SendActivationCodeResponse> sendActivationCode(@h("VND.se.avanza.security-TwoFactor-Activation-Transaction-Id") String str);

    @m("/_api/authentication/enabledevicetoken/verify-activationcode")
    Single<VerifyActivationCodeResponse> verifyActivationCode(@a VerifyActivationCodeRequest verifyActivationCodeRequest, @h("VND.se.avanza.security-TwoFactor-Activation-Transaction-Id") String str);

    @m("/_api/authentication/sessions/totp")
    Single<TotpAuthentication> verifyTotp(@a TotpVerify totpVerify, @h("VND.se.avanza.security-Totp-Transaction-Id") TwofactorTransactionId twofactorTransactionId);
}
