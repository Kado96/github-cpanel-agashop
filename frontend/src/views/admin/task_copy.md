# AgaShop Chatbot & UI Refinement Task

## Objective
Activate the chatbot, enhance its dialogue to feel like ChatGPT, and fix pending UI warnings.

## Tasks
- [x] Standardize chatbot introduction across all pages <!-- id: 61 -->
- [x] Implement FAB collision detection for chatbot positioning <!-- id: 62 -->
- [x] Add/Refine help coverage for all statistics sub-modules <!-- id: 63 -->
- [x] Verify chatbot presence on all key pages <!-- id: 64 -->
- [x] Standardize Login and Register introductions
- [x] Standardize Home, Admin, and Agent introductions with exhaustive "explain all" content <!-- id: 65 -->
- [x] Verify route mapping and automatic help context updates in router <!-- id: 66 -->
- [x] Clean raw HTML tags from notifications, alerts, and UI components
    - [x] Identify all occurrences of `<br>`, `<strong>`, `<code>` in strings
    - [x] Replace HTML tags with `\n` or standard UI components for better alignment
    - [x] Verify fix in `ShopHome.vue` (Premium Alert)
    - [x] Verify fix in `Admin` views (Password alerts)
    - [x] Verify fix in `axios.js` (Error alerts)
    - [x] Verify fix in `ContextualHelpBot.vue` (Dynamic messages)
    - [x] Standardize template tags (strong, em) to CSS classes in `ShopHome.vue`, `ShopStats.vue`, `PaymentMethods.vue`, `OTPPage.vue`, `UserForm.vue`, `ContextualHelpBot.vue`
    - [x] Add error resilience in `ShopStats.vue` fetchStats
    - [x] Remove "Subscription Required" popup in `ShopStats.vue`
    - [x] Redirect Premium banner in `ShopHome.vue` to `payment-methods`
    - [x] Redirect statistics 403 error in `ShopStats.vue` to `payment-methods`
- [x] Implement better conversational flow for manual questions <!-- id: 59 -->
- [x] Verify chat responsiveness on various pages <!-- id: 60 -->
- [x] Audit Sales/Control/Product pages and update help documentation with technical accuracy
- [x] Update all remaining pages (Expenses, Supplies, Stats, Payment Methods) with exhaustive help documentation
- [x] Verify technical accuracy of all chatbot dialogues against actual code implementation
- [/] Modernize Application Headers for Professional UI/UX
    - [x] Define global CSS for professional header styling
    - [/] Fix `ion-title` nesting in `ShopProducts.vue` and improve count display
    - [x] Fix `ion-title` nesting and styling in `SupplyProducts.vue`
    - [x] Fix `ion-title` nesting and styling in `SalesProducts.vue`
    - [x] Audit and fix other views (Expenses, Controls, ProfilPage)
- [x] Finalize `walkthrough.md` with proof of documentation quality
