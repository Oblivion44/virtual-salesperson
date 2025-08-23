# Shopping Cart Unit

## Overview
This bounded context manages the shopping cart functionality, including adding/removing products, quantity management, pricing calculations, and checkout processes.

## Bounded Context Scope
- Shopping cart state management
- Product quantity and pricing calculations
- Cart persistence during sessions
- Checkout process and validation
- Cart-related user interface components

## User Stories Included

### US-009: Add Products to Cart
**As a** user interested in purchasing products  
**I want to** add recommended products to my shopping cart  
**So that** I can collect items for purchase  

**Acceptance Criteria:**
- [ ] User can add products to cart from recommendation display
- [ ] User can add products to cart from detail view
- [ ] System confirms when product is added to cart
- [ ] System handles duplicate products by updating quantity
- [ ] Cart maintains product information (name, price, image, etc.)

### US-010: Cart Management and Checkout
**As a** user with items in my cart  
**I want to** view, modify, and checkout my selected products  
**So that** I can complete my purchase  

**Acceptance Criteria:**
- [ ] User can view all items in cart with quantities and prices
- [ ] User can see total cart value
- [ ] User can remove items from cart
- [ ] User can clear entire cart
- [ ] User can proceed to checkout
- [ ] System provides checkout confirmation
- [ ] Cart is cleared after successful checkout

## Domain Concepts

### Core Entities
- **ShoppingCart**: The main cart entity containing all cart items and metadata
- **CartItem**: Individual product in the cart with quantity and pricing information

### Value Objects
- **CartId**: Unique identifier for shopping carts
- **ProductId**: Reference to products in the cart
- **Quantity**: Number of items (positive integer)
- **ItemPrice**: Price per individual item
- **LineTotal**: Total price for a cart line (quantity × item price)
- **CartTotal**: Total value of entire cart
- **CartStatus**: Current state of the cart (Active, Checkout, Completed, Abandoned)

### Aggregates
- **ShoppingCartAggregate**: Root aggregate managing cart state and operations

### Domain Services
- **CartCalculationService**: Handles all pricing and total calculations
- **CartValidationService**: Validates cart operations and constraints
- **CheckoutService**: Manages the checkout process and validation

### Repositories
- **ShoppingCartRepository**: Manages cart persistence and retrieval

### Domain Events
- **ProductAddedToCart**: When a product is added to the cart
- **ProductRemovedFromCart**: When a product is removed from the cart
- **CartQuantityUpdated**: When item quantity is changed
- **CartCleared**: When entire cart is emptied
- **CheckoutInitiated**: When checkout process begins
- **CheckoutCompleted**: When checkout is successfully completed
- **CartAbandoned**: When cart is left inactive for extended period

## External Dependencies
- **Product Recommendation Unit**: For product information and pricing
- **User Profile Unit**: For user information during checkout
- **Conversation Management Unit**: For cart status updates in chat

## Interface Contracts

### Inbound
- `addProductToCart(cartId: CartId, productId: ProductId, quantity: Quantity): CartItem`
- `removeProductFromCart(cartId: CartId, productId: ProductId): void`
- `updateQuantity(cartId: CartId, productId: ProductId, quantity: Quantity): CartItem`
- `getCart(cartId: CartId): ShoppingCart`
- `clearCart(cartId: CartId): void`
- `calculateCartTotal(cartId: CartId): CartTotal`
- `initiateCheckout(cartId: CartId): CheckoutSession`
- `completeCheckout(cartId: CartId, paymentInfo: PaymentInfo): CheckoutResult`

### Outbound
- `getProductInfo(productId: ProductId): ProductInfo`
- `validateProductAvailability(productId: ProductId, quantity: Quantity): boolean`
- `getUserProfile(userId: UserId): UserProfile`

## Business Rules

### Cart Operations
1. **Add Product**: 
   - Product must exist and be available
   - If product already in cart, increase quantity instead of creating duplicate
   - Maximum quantity per item is 10
   - Cart can contain maximum 20 different products

2. **Remove Product**:
   - Product must exist in cart
   - Removing product updates cart totals immediately
   - Cart can be empty after removal

3. **Update Quantity**:
   - Quantity must be positive integer (1-10)
   - Setting quantity to 0 removes the item
   - Quantity changes update totals immediately

4. **Cart Totals**:
   - Line total = quantity × current product price
   - Cart total = sum of all line totals
   - Prices must be calculated in real-time (no caching)

### Checkout Rules
1. **Checkout Validation**:
   - Cart must not be empty
   - All products must still be available
   - User profile must be complete (for shipping/billing)
   - Total must be recalculated before checkout

2. **Checkout Process**:
   - Cart is locked during checkout (no modifications allowed)
   - Successful checkout clears the cart
   - Failed checkout unlocks cart for modifications
   - Checkout generates confirmation with order details

### Session Management
1. **Cart Persistence**:
   - Cart persists throughout user session
   - Cart is associated with session, not permanent user account
   - Cart expires when session ends
   - No cross-session cart persistence

2. **Cart State**:
   - Active: Normal cart operations allowed
   - Checkout: Cart locked, only checkout operations allowed
   - Completed: Cart cleared, read-only for confirmation
   - Abandoned: Session ended, cart no longer accessible

## Cart Calculation Logic

### Price Calculations
```
Line Total = Quantity × Current Product Price
Subtotal = Sum of all Line Totals
Tax = Subtotal × Tax Rate (if applicable)
Shipping = Calculated based on location and total (if applicable)
Cart Total = Subtotal + Tax + Shipping
```

### Discount Logic (Future Enhancement)
- Volume discounts for multiple items
- Category-based discounts
- User profile-based discounts (student, professional)
- Promotional codes and coupons

## User Interface Integration

### Cart Display Components
- **Cart Summary**: Shows item count and total value
- **Cart Details**: Full list of items with quantities and prices
- **Item Controls**: Add/remove/update quantity buttons
- **Checkout Button**: Initiates checkout process
- **Clear Cart**: Empties entire cart with confirmation

### Cart Status Indicators
- **Empty Cart**: "Your cart is empty" message
- **Item Count**: "Cart (X items)" display
- **Total Value**: Prominent total price display
- **Checkout Status**: Progress indicators during checkout

## Error Handling

### Common Error Scenarios
1. **Product Not Available**: Handle gracefully with user notification
2. **Quantity Limits**: Prevent exceeding maximum quantities
3. **Price Changes**: Notify user if prices change during session
4. **Checkout Failures**: Provide clear error messages and recovery options
5. **Session Expiry**: Handle cart loss gracefully with appropriate messaging

### Error Recovery
- **Product Unavailable**: Offer similar product suggestions
- **Price Increases**: Allow user to confirm or remove item
- **Checkout Failure**: Return to cart with error explanation
- **Session Loss**: Offer to recreate cart from conversation history

## Quality Attributes
- **Performance**: Cart operations must complete within 200ms
- **Reliability**: Cart state must be consistent and never corrupted
- **Usability**: Cart interface must be intuitive and responsive
- **Accuracy**: Price calculations must be precise and real-time
