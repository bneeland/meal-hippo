product
-name
-description

price
---product
-currency

plan
---product
---price
-interval

subscription_item
---plan
---subscription
-quantity

subscription
---customer
---subscription_item(s)
-cancel_at
-period_start/period_end

customer
-email
---source(s)

source
---customer

----------------------

Item (aka Membership)
-slug (new)
-name (existing; aka "type")
-price (existing)
-stripe plan id (new)

UserSubscription (aka UserMembership)
-user
-stripe customer id
-subscription_items (items, aka "membership type")
