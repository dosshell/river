package se.avanza.android.api.retrofit;

import com.google.firebase.analytics.FirebaseAnalytics;
import io.reactivex.Completable;
import io.reactivex.Single;
import java.util.ArrayList;
import java.util.List;
import kotlin.jvm.internal.h;
import okhttp3.e0;
import org.joda.time.LocalDate;
import retrofit2.t.a;
import retrofit2.t.e;
import retrofit2.t.m;
import retrofit2.t.n;
import retrofit2.t.q;
import retrofit2.t.r;
import se.avanza.android.api.domain.constants.TransactionFilterType;
import se.avanza.android.api.domain.models.common.AccountId;
import se.avanza.android.api.domain.models.common.OrderbookId;
import se.avanza.android.api.models.account.AccountPositions;
import se.avanza.android.api.models.account.AccountTypeIdentifier;
import se.avanza.android.api.models.account.AggregatedAccountOverview;
import se.avanza.android.api.models.account.EventCount;
import se.avanza.android.api.models.account.OverviewCategory;
import se.avanza.android.api.models.dealsandorders.DealsAndOrders;
import se.avanza.android.api.models.monthlysavings.ExternalAccount;
import se.avanza.android.api.models.monthlysavings.MonthlySavingsAccount;
import se.avanza.android.api.models.order.OrderAccount;
import se.avanza.android.api.models.transactions.IsinAndCurrency;
import se.avanza.android.api.models.transactions.TransactionFilterValues;
import se.avanza.android.api.models.transactions.TransactionsResponse;
import se.avanza.android.api.models.transfer.DepositAccount;

/* compiled from: AccountApi.kt */
public interface AccountApi {

    /* compiled from: AccountApi.kt */
    public static final class CategoryId {
        private final String categoryId;

        public CategoryId(String str) {
            h.b(str, "categoryId");
            this.categoryId = str;
        }

        public static /* synthetic */ CategoryId copy$default(CategoryId categoryId2, String str, int i2, Object obj) {
            if ((i2 & 1) != 0) {
                str = categoryId2.categoryId;
            }
            return categoryId2.copy(str);
        }

        public final String component1() {
            return this.categoryId;
        }

        public final CategoryId copy(String str) {
            h.b(str, "categoryId");
            return new CategoryId(str);
        }

        public boolean equals(Object obj) {
            return this == obj || ((obj instanceof CategoryId) && h.a((Object) this.categoryId, (Object) ((CategoryId) obj).categoryId));
        }

        public final String getCategoryId() {
            return this.categoryId;
        }

        public int hashCode() {
            String str = this.categoryId;
            if (str != null) {
                return str.hashCode();
            }
            return 0;
        }

        public String toString() {
            return "CategoryId(categoryId=" + this.categoryId + ")";
        }
    }

    /* compiled from: AccountApi.kt */
    public static final class DisplayBuyingPowerWithCredit {
        private final String value;

        public DisplayBuyingPowerWithCredit(String str) {
            h.b(str, FirebaseAnalytics.b.VALUE);
            this.value = str;
        }

        public static /* synthetic */ DisplayBuyingPowerWithCredit copy$default(DisplayBuyingPowerWithCredit displayBuyingPowerWithCredit, String str, int i2, Object obj) {
            if ((i2 & 1) != 0) {
                str = displayBuyingPowerWithCredit.value;
            }
            return displayBuyingPowerWithCredit.copy(str);
        }

        public final String component1() {
            return this.value;
        }

        public final DisplayBuyingPowerWithCredit copy(String str) {
            h.b(str, FirebaseAnalytics.b.VALUE);
            return new DisplayBuyingPowerWithCredit(str);
        }

        public boolean equals(Object obj) {
            return this == obj || ((obj instanceof DisplayBuyingPowerWithCredit) && h.a((Object) this.value, (Object) ((DisplayBuyingPowerWithCredit) obj).value));
        }

        public final String getValue() {
            return this.value;
        }

        public int hashCode() {
            String str = this.value;
            if (str != null) {
                return str.hashCode();
            }
            return 0;
        }

        public String toString() {
            return "DisplayBuyingPowerWithCredit(value=" + this.value + ")";
        }

        public DisplayBuyingPowerWithCredit(boolean z) {
            this(String.valueOf(z));
        }
    }

    @e("/_mobile/account/overview")
    Single<AggregatedAccountOverview> accountOverview();

    @e("/_mobile/account/dealsandorders")
    Single<DealsAndOrders> dealsAndOrders();

    @e("/_mobile/account/list?onlyDepositable=true")
    Single<ArrayList<DepositAccount>> depositableAccounts();

    @e("/_mobile/account/list?onlyTrustlyDepositable=true")
    Single<ArrayList<DepositAccount>> depositableTrustlyAccounts();

    @e("/_mobile/transfer/external-accounts")
    Single<ArrayList<ExternalAccount>> externalAccounts();

    @e("/_cqbe/ff/overview/categories")
    Single<OverviewCategory> getAccountCategories();

    @e("/_mobile/account/{accountId}/overview")
    Single<AccountTypeIdentifier> getAccountOverview(@q("accountId") AccountId accountId);

    @e("/_mobile/account/{accountId}/positions")
    Single<AccountPositions> getAccountPositions(@q("accountId") AccountId accountId, @r("autoPortfolio") boolean z);

    @e("/_mobile/account/positions")
    Single<AccountPositions> getAccountPositions(@r("aggregate") boolean z, @r("autoPortfolio") boolean z2);

    @e("/_mobile/account/list")
    Single<List<OrderAccount>> getAccountsWithPosition(@r("orderbookId") OrderbookId orderbookId);

    @e("/_mobile/account/list?onlyForAuto=true")
    Single<List<MonthlySavingsAccount>> getAutoAccounts();

    @e("/_mobile/account/contractnote/{accountId}/{noteId}.pdf")
    Single<e0> getContractNote(@q("accountId") AccountId accountId, @q("noteId") String str);

    @e("/_mobile/account/dealsandorders/{accountId}")
    Single<DealsAndOrders> getDealsAndOrders(@q("accountId") AccountId accountId);

    @e("/_mobile/account/list?onlyForMonthlySavings=true")
    Single<List<MonthlySavingsAccount>> getMonthlySavingsAccounts();

    @e("/_mobile/account/list")
    Single<List<OrderAccount>> getTradableAccounts(@r("onlyTradable") boolean z);

    @e("/_mobile/account/transactions/{transactionType}")
    Single<TransactionsResponse> getTransactions(@q("transactionType") TransactionFilterType transactionFilterType, @r("from") LocalDate localDate, @r("to") LocalDate localDate2, @r("isinAndCurrency") CommaSeparatedPath<IsinAndCurrency> commaSeparatedPath, @r("orderbookId") CommaSeparatedPath<OrderbookId> commaSeparatedPath2);

    @e("/_mobile/account/transactions/{accountId}/{transactionType}")
    Single<TransactionsResponse> getTransactions(@q("accountId") AccountId accountId, @q("transactionType") TransactionFilterType transactionFilterType, @r("from") LocalDate localDate, @r("to") LocalDate localDate2, @r("isinAndCurrency") CommaSeparatedPath<IsinAndCurrency> commaSeparatedPath, @r("orderbookId") CommaSeparatedPath<OrderbookId> commaSeparatedPath2);

    @e("/_mobile/account/transactions/options")
    Single<TransactionFilterValues> getTransactionsFilterValues(@r("from") LocalDate localDate, @r("to") LocalDate localDate2, @r("includeInstrumentsWithNoOrderbook") boolean z);

    @n("/_api/usercontent/account/{accountId}")
    Completable renameAccount(@q("accountId") AccountId accountId, @r("name") String str);

    @m("/_cqbe/ff/account/{accountId}/category-id")
    Completable setAccountCategory(@q("accountId") AccountId accountId, @a CategoryId categoryId);

    @m("/_cqbe/ff/account/settings/{accountId}/DISPLAY_BUYING_POWER_WITH_CREDIT")
    Completable setDisplayBuyingPowerWithCredit(@q("accountId") AccountId accountId, @a DisplayBuyingPowerWithCredit displayBuyingPowerWithCredit);

    @e("/_mobile/account/transactions")
    Single<TransactionsResponse> transactions();

    @e("/_mobile/account/eventcount")
    Single<EventCount> transactionsEventCount();

    @e("_mobile/account/{accountId}/eventcount")
    Single<EventCount> transactionsEventCount(@q("accountId") AccountId accountId);
}
