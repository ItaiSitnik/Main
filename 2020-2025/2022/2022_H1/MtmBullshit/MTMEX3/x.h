#ifndef EX3_QUEUE_H
#define EX3_QUEUE_H

template <class T>
class Queue {

public:
    // Empty c'tor for an empty queue
    Queue();

    // Recieves new element and pushes it to the back of the queue
    void pushBack(const T& data);

    // Returns the node at the front of the queue
    T& front();
    const T& front() const;

    // Removes front node from queue
    void popFront();

    // Returns number of nodes in queue
    int size() const;

    // Copy c'tor, d'tor, = operator to the queue
    Queue(const Queue&);
    ~Queue();
    Queue& operator=(const Queue&);

    // Iterator and ConstIterator classes for the queue
    class Iterator;
    class ConstIterator;

    // Return Iterator classes that point to the beginning of the queue
    Iterator begin();
    ConstIterator begin() const;

    // Return Iterator classes that point to the end of the queue
    Iterator end();
    ConstIterator end() const;

    class EmptyQueue {
    };

private:
    // Node class to implement the queue as a linked list
    struct Node {
        T data;
        Node* next;
    };

    // Pointers to the links of the front and the rear of the queue
    Node* m_front;
    Node* m_rear;

    //
    void deleteList();
};

template <class T>
Queue<T>::Queue()
    : m_front(nullptr)
    , m_rear(nullptr)
{
}

template <class T>
void Queue<T>::pushBack(const T& data)
{
    Node* append = new Node;
    append->data = data;
    append->next = nullptr;

    if (m_front == nullptr) {
        m_front = m_rear = append;
    } else {
        m_rear->next = append;
        m_rear = m_rear->next;
    }
}

template <class T>
T& Queue<T>::front()
{
    if (m_front == nullptr) {
        throw EmptyQueue();
    }
    return m_front->data;
}

template <class T>
const T& Queue<T>::front() const
{
    if (m_front == nullptr) {
        throw EmptyQueue();
    }
    return m_front->data;
}

template <class T>
void Queue<T>::popFront()
{
    if (m_front == nullptr) {
        throw EmptyQueue();
    }
    Node* toDelete = m_front;
    m_front = m_front->next;
    delete toDelete;
}

template <class T>
int Queue<T>::size() const
{
    int size = 0;
    for (typename Queue<T>::ConstIterator i = queue.begin(); i != queue.end(); ++i) {
        size++;
    }
    return size;
}

// Function object that receives a and builds a new queue containing all the nodes
// that answer the condition of the boolean function
template <class T>
Queue<T> filter(Queue<T> queue, bool (*function)(T))
{
    Queue<T> out;
    for (T t : queue) {
        if (function(t)) {
            out.pushBack(t);
        }
    }
    return out;
}

// Function object that recives a queue and transformation function and do the
// function on every element in the queue
template <class T>
Queue<T> transform(Queue<T> queue, void (*function)(T&))
{
    for (typename Queue<T>::Iterator i = queue.begin(); i != queue.end(); ++i) {
        fucntion(*i);
    }
}

template <class T>
Queue<T>::Queue(const Queue<T>& other)
{
    m_front = m_rear = nullptr;
    for (T t : other) {
        pushBack(t);
    }
}

template <class T>
Queue<T>::~Queue()
{
    deleteList();
}

template <class T>
Queue<T>& Queue<T>::operator=(Queue const& other)
{
    if (this == &other) {
        return *this;
    }
    deleteList();
    for (T t : other) {
        pushBack(t);
    }
}

template <class T>
void Queue<T>::deleteList()
{
    while (m_front != nullptr) {
        popFront();
    }
}

template <class T>
typename Queue<T>::Iterator Queue<T>::begin()
{
    return Iterator(m_front);
}

template <class T>
typename Queue<T>::ConstIterator Queue<T>::begin() const
{
    return ConstIterator(m_front);
}

template <class T>
typename Queue<T>::Iterator Queue<T>::end()
{
    return Iterator(nullptr);
}

template <class T>
typename Queue<T>::ConstIterator Queue<T>::end() const
{
    return ConstIterator(nullptr);
}

// Iterator class code

template <class T>
class Queue<T>::Iterator {

public:
    // Overloading operator to set current instance to the next link
    Iterator& operator++();
    // Overloading operator for a bool to check if two iterators are
    // pointing at the same link
    bool operator!=(const Iterator& other) const;
    // Overloading operator for getting the current iterator link data
    T& operator*() const;

    // Class exception for invalid operations on this iterator
    class InvalidOperation {
    };

    //
    Iterator(const Iterator&) = default;
    ~Iterator() = default;
    Iterator& operator=(const Iterator&) = default;

private:
    Node* m_current;
    Iterator(Node* node);
    friend class Queue<T>;
};

template <class T>
Queue<T>::Iterator& Queue<T>::Iterator::operator++()
{
    m_current = m_current->next;
}

template <class T>
bool Queue<T>::Iterator::operator!=(const Iterator& other) const
{
    if (m_current == nullptr && other.m_current == nullptr) {
        return false;
    }
    if ((m_current == nullptr) ^ (other.m_current == nullptr)) {
        return true;
    }
    return m_current->data == other.m_current->data && m_current->next == other.m_current->next;
}

template <class T>
T& Queue<T>::Iterator::operator*() const
{
    return m_current->data;
}

template <class T>
Queue<T>::Iterator::Iterator(Node* node)
    : m_current(node)
{
}

// ConstIterator class code

template <class T>
class Queue<T>::ConstIterator {

public:
    // Overloading operator to set current instance to the next link
    ConstIterator& operator++();
    // Overloading operator for a bool to check if two iterators are
    // pointing at the same link
    bool operator!=(const ConstIterator& other) const;
    // Overloading operator for getting the current iterator link data
    const T& operator*() const;

    // Class exception for invalid operations on this iterator
    class InvalidOperation {
    };

    ConstIterator(const ConstIterator&) = default;
    ~ConstIterator() = default;
    ConstIterator& operator=(const ConstIterator&) = default;

private:
    Node* m_current;
    ConstIterator(Node* node);
    friend class Queue<T>;
};

template <class T>
Queue<T>::ConstIterator& Queue<T>::ConstIterator::operator++()
{
    m_current = m_current->next;
}

template <class T>
bool Queue<T>::ConstIterator::operator!=(const ConstIterator& other) const
{
    if (m_current == nullptr && other.m_current == nullptr) {
        return false;
    }
    if ((m_current == nullptr) ^ (other.m_current == nullptr)) {
        return true;
    }
    return m_current->data == other.m_current->data && m_current->next == other.m_current->next;
}

template <class T>
const T& Queue<T>::ConstIterator::operator*() const
{
    return m_current->data;
}

template <class T>
Queue<T>::ConstIterator::ConstIterator(Node* node)
    : m_current(node)
{
}

#endif // EX3_QUEUE_H
