package se.avanza.android.api.retrofit;

import io.reactivex.Completable;
import io.reactivex.Single;
import java.util.List;
import retrofit2.t.a;
import retrofit2.t.e;
import retrofit2.t.m;
import retrofit2.t.q;
import retrofit2.t.r;
import se.avanza.android.api.domain.models.common.AccountId;
import se.avanza.android.api.domain.models.common.TrustlyTransactionId;
import se.avanza.android.api.models.monthlysavings.ExternalAccount;
import se.avanza.android.api.models.transfer.TransferAccount;
import se.avanza.android.api.models.transfer.TransferCreationRequest;
import se.avanza.android.api.models.transfer.TransferCreationResponse;
import se.avanza.android.api.models.transfer.TransferList;
import se.avanza.android.api.models.transfer.external.WithdrawProfile;
import se.avanza.android.api.models.transfer.external.WithdrawQuarantine;
import se.avanza.android.api.models.transfer.external.WithdrawResult;
import se.avanza.android.api.models.transfer.external.WithdrawSmsBody;
import se.avanza.android.api.models.transfer.external.WithdrawalRequest;
import se.avanza.android.api.models.transfer.internal.InternalTransferStatus;
import se.avanza.android.api.models.transfer.internal.InternalTransferValidationRequest;
import se.avanza.android.api.models.transfer.internal.InternalTransferValidationResult;
import se.avanza.android.api.models.transfer.trustly.InitializeTrustlyDepositResponse;
import se.avanza.android.api.models.transfer.trustly.TransferAvailability;
import se.avanza.android.api.models.transfer.trustly.TrustlyDepositRequest;
import se.avanza.android.api.models.transfer.trustly.TrustlyDepositStatus;
import se.avanza.android.api.models.transfer.trustly.TrustlyRequestStatus;

/* compiled from: TransferApi.kt */
public interface TransferApi {
    @e("/_mobile/transfer/availability")
    Single<TransferAvailability> availability();

    @m("/_api/transfer/internal/create")
    Single<TransferCreationResponse> createTransfer(@a TransferCreationRequest transferCreationRequest);

    @m("/_api/transfer/trustly/")
    Single<InitializeTrustlyDepositResponse> createTrustlyDeposit(@a TrustlyDepositRequest trustlyDepositRequest);

    @e("/_mobile/transfer/external-accounts")
    Single<List<ExternalAccount>> externalAccounts();

    @e("/_mobile/transfer/internal/from-accounts/{toAccountId}")
    Single<List<TransferAccount>> getInternalTransferFromAccounts(@q("toAccountId") AccountId accountId);

    @e("/_mobile/transfer/transfers/list/{accountId}")
    Single<TransferList> getTransferList(@q("accountId") AccountId accountId);

    @m("/_api/transfer/internal/status")
    Single<InternalTransferStatus> getTransferStatus(@r("transferId") String str, @r("fromAccountId") AccountId accountId);

    @e("/_mobile/transfer/trustly/{transactionId}")
    Single<TrustlyDepositStatus> getTrustlyDepositStatus(@q("transactionId") TrustlyTransactionId trustlyTransactionId);

    @e("/_api/transfer/trustly/{transactionId}")
    Single<TrustlyRequestStatus> getTrustlyRequestStatus(@q("transactionId") TrustlyTransactionId trustlyTransactionId);

    @e("/_mobile/transfer/withdrawability/from/{accountId}")
    Single<List<ExternalAccount>> getWithdrawExternalAccounts(@q("accountId") AccountId accountId);

    @e("/_mobile/transfer/withdrawability/from/quarantine")
    Single<WithdrawQuarantine> getWithdrawalQuarantine();

    @m("/_mobile/transfer/withdrawal")
    Single<WithdrawResult> sendWithdrawalRequest(@a WithdrawalRequest withdrawalRequest);

    @m("/_mobile/transfer/withdrawal/sms/send")
    Completable sendWithdrawalSmsCode(@a WithdrawSmsBody withdrawSmsBody);

    @e("/_mobile/transfer/validate-external-account/{accountnumber}")
    Single<ExternalAccount> validateExternalAccount(@q("accountnumber") String str);

    @m("/_mobile/transfer/internal/validate")
    Single<InternalTransferValidationResult> validateInternalTransfer(@a InternalTransferValidationRequest internalTransferValidationRequest);

    @e("/_mobile/transfer/withdrawability/from/list")
    Single<WithdrawProfile> withdrawableAccounts();
}
