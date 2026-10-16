#ifndef EX3_QUEUE_H
#define EX3_QUEUE_H

#include <iostream>
#include <new>

template <class T>
class Queue {

public:
    Queue();

    void pushBack(const T& value);
    T& front();
    const T& front() const;
    void popFront();
    int size() const;

    Queue(Queue const& queue);
    ~Queue();
    Queue& operator=(const Queue& queue);

    class Iterator;
    class ConstIterator;

    Iterator begin();
    ConstIterator begin() const;

    Iterator end();
    ConstIterator end() const;

    class EmptyQueue {
    };

private:
    struct Node {
        T data;
        Node* next;
    };
    Node* m_front;
    Node* m_rear;

    void deleteList();
};

template <class T>
Queue<T>::Queue()
    : m_front(nullptr)
    , m_rear(nullptr)
{
}

template <class T>
void Queue<T>::pushBack(const T& value)
{
    Node* append = new Node;
    append->data = value;
    append->next = nullptr;

    if (m_front == nullptr) {
        m_front = m_rear = append;
    } else {
        m_rear->next = append;
        m_rear = append;
    }
}

template <class T>
T& Queue<T>::front()
{
    if (m_front == nullptr) {
        throw Queue<T>::EmptyQueue();
    }
    return m_front->data;
}

template <class T>
const T& Queue<T>::front() const
{
    if (m_front == nullptr) {
        throw Queue<T>::EmptyQueue();
    }
    return m_front->data;
}

template <class T>
void Queue<T>::popFront()
{
    Node* toDelete = m_front;
    m_front = m_front->next;
    delete toDelete;
}

template <class T>
int Queue<T>::size() const
{
    int size = 0;
    for (typename Queue<T>::ConstIterator i = begin(); i != end(); ++i) {
        size++;
    }
    return size;
}

template <class T>
Queue<T> filter(const Queue<T>& queue, bool (*function)(T))
{
    Queue<T> out;
    for (T t : queue) {
        if (function(t)) {
            out.pushBack(t);
        }
    }
    return out;
}

template <class T>
void transform(Queue<T>& queue, void (*function)(T&))
{
    for (typename Queue<T>::Iterator i = queue.begin(); i != queue.end(); ++i) {
        function(*i);
    }
}

template <class T>
Queue<T>::Queue(Queue const& queue)
{
    m_front = m_rear = nullptr;
    for (T t : queue) {
        pushBack(t);
    }
}

template <class T>
Queue<T>::~Queue<T>()
{
    deleteList();
}

template <class T>
Queue<T>& Queue<T>::operator=(const Queue<T>& queue)
{
    if (this == &queue) {
        return *this;
    }
    deleteList();
    for (typename Queue<T>::ConstIterator i = queue.begin(); i != queue.end(); ++i) {
        pushBack(*i);
    }
    return *this;
}

// ITERATOR CODE

template <class T>
class Queue<T>::Iterator {

public:
    Iterator& operator++();
    bool operator!=(const Iterator& other) const;
    T& operator*() const;

    class InvalidOperation {
    };

    Iterator(const Iterator&) = default;
    Iterator& operator=(const Iterator&) = default;

private:
    Node* m_current;
    Iterator(Node* node);
    friend class Queue<T>;
};

template <class T>
typename Queue<T>::Iterator& Queue<T>::Iterator::operator++()
{
    if (m_current == nullptr) {
        throw InvalidOperation();
    }
    m_current = m_current->next;
    return *this;
}

template <class T>
bool Queue<T>::Iterator::operator!=(const Queue<T>::Iterator& other) const
{
    if (m_current == nullptr && other.m_current == nullptr) {
        return false;
    }
    if ((m_current == nullptr) ^ (other.m_current == nullptr)) {
        return true;
    }
    return m_current->data != other.m_current->data || m_current->next != other.m_current->next;
}

template <class T>
T& Queue<T>::Iterator::operator*() const
{
    if (m_current == nullptr) {
        throw InvalidOperation();
    }
    return m_current->data;
}

template <class T>
Queue<T>::Iterator::Iterator(Node* node)
    : m_current(node)
{
}

// CONSTITERATOR CODE

template <class T>
class Queue<T>::ConstIterator {

public:
    ConstIterator& operator++();
    bool operator!=(const ConstIterator& other) const;
    const T& operator*() const;

    ConstIterator(const ConstIterator&) = default;
    ConstIterator& operator=(const ConstIterator&) = default;

    class InvalidOperation {
    };

private:
    Node* m_current;
    ConstIterator(Node* node);
    friend class Queue<T>;
};

template <class T>
typename Queue<T>::ConstIterator& Queue<T>::ConstIterator::operator++()
{
    if (m_current == nullptr) {
        throw InvalidOperation();
    }
    m_current = m_current->next;
    return *this;
}

template <class T>
bool Queue<T>::ConstIterator::operator!=(const Queue<T>::ConstIterator& other) const
{
    if (m_current == nullptr && other.m_current == nullptr) {
        return false;
    }
    if ((m_current == nullptr) ^ (other.m_current == nullptr)) {
        return true;
    }
    return m_current->data != other.m_current->data || m_current->next != other.m_current->next;
}

template <class T>
const T& Queue<T>::ConstIterator::operator*() const
{
    if (m_current == nullptr) {
        throw InvalidOperation();
    }
    const T& out = m_current->data;
    return out;
}

template <class T>
Queue<T>::ConstIterator::ConstIterator(Node* node)
    : m_current(node)
{
}

// REST OF QUEUE

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

template <class T>
void Queue<T>::deleteList()
{
    while (m_front != nullptr) {
        popFront();
    }
}

#endif // EX3_QUEUE_H
