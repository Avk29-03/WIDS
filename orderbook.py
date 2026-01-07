from bisect import bisect_left, insort
class Order:
    def __init__(self, order_id, side, price, qty, timestamp):
        self.id, self.side, self.price, self.qty, self.timestamp = order_id, side, price, qty, timestamp
        self.next = None
        self.prev = None
        self.limit = None
class Limit:
    def __init__(self,price):
        self.price = price
        self.head = None
        self.tail = None
        self.total_qty = 0
    def append(self, order):
        order.limit = self

        if self.tail is None:
            self.head = self.tail = order
        else:
            order.prev = self.tail
            self.tail.next = order
            self.tail = order

        self.total_qty += order.qty
    def remove(self, order):
        if order.prev:
            order.prev.next = order.next
        else:
            self.head = order.next

        if order.next:
            order.next.prev = order.prev
        else:
            self.tail = order.prev

        self.total_qty -= order.qty

        order.prev = None
        order.next = None
        order.limit = None
    def pop_head(self):
        if self.head is None:
            return None

        order = self.head
        self.remove(order)
        return order
    def get_head_order(self):
        return self.head
class BookSide:
    def __init__(self, ascending=True):
        self.limits = {}
        self.prices = []
        self.ascending = ascending
    def get_or_create_limit(self, price):
        if price not in self.limits:
            limit = Limit(price)
            self.limits[price] = limit
            insort(self.prices, price)
        return self.limits[price]
    def remove_limit_if_empty(self, limit):
        if limit.total_qty == 0:
            del self.limits[limit.price]
            idx = bisect_left(self.prices, limit.price)
            self.prices.pop(idx)
    def best_price(self):
        if not self.prices:
            return None
        if self.ascending:
            return self.prices[0]
        else:
            return self.prices[-1]
    def best_limit(self):
        price = self.best_price()
        if price is None:
            return None
        else:
            return self.limits[price]



class OrderBook:
    def __init__(self):
        self.buys = BookSide(ascending=False)
        self.sells = BookSide(ascending=True)

        self.order_map = {}
        self.trades = []
    def _match_buy(self, order):
        while order.qty > 0:
            best_price = self.sells.best_price()
            if best_price is None:
                break
            if order.price is not None and best_price > order.price:
                break
            limit = self.sells.limits[best_price]
            resting = limit.head
            if resting is None:
    
                self.buys.remove_limit_if_empty(limit)
                break
            trade_qty = min(order.qty, resting.qty)

            order.qty -= trade_qty
            resting.qty -= trade_qty
            limit.total_qty -= trade_qty

            self.trades.append(
                (order.id, resting.id, best_price, trade_qty)
            )

            if resting.qty == 0:
                limit.remove(resting)
                del self.order_map[resting.id]
                self.sells.remove_limit_if_empty(limit)
    def _match_sell(self, order):
        while order.qty > 0:
            best_price = self.buys.best_price()
            if best_price is None:
                break
            if order.price is not None and best_price < order.price:
                break
            limit = self.buys.limits[best_price]
            resting = limit.head
            if resting is None:
                self.buys.remove_limit_if_empty(limit)
                break

            trade_qty = min(order.qty, resting.qty)

            order.qty -= trade_qty
            resting.qty -= trade_qty

            self.trades.append(
                (resting.id, order.id, best_price, trade_qty)
            )

            if resting.qty == 0:
                limit.remove(resting)
                del self.order_map[resting.id]
                self.buys.remove_limit_if_empty(limit)
    def add_order(self, order):
        if order.side == "B":
            self._match_buy(order)
        else:
            self._match_sell(order)

        if order.qty > 0 and order.price is not None:
            self._add_to_book(order)
    def _add_to_book(self, order):
        side = self.buys if order.side == "B" else self.sells
        limit = side.get_or_create_limit(order.price)
        limit.append(order)
        self.order_map[order.id] = order
    def cancel(self, order_id):
        order = self.order_map.get(order_id)
        if not order:
            return

        limit = order.limit
        limit.remove(order)

        side = self.buys if order.side == "B" else self.sells
        side.remove_limit_if_empty(limit)

        del self.order_map[order_id]
    def depth(self, side, n=5):
        book = self.buys if side == "B" else self.sells
        if side == "B":
            prices = book.prices[-n:][::-1]
        else:
            prices = book.prices[:n]

        return [(p, book.limits[p].total_qty) for p in prices]
