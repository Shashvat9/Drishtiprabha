#include <iostream>
#include <unordered_map>
using namespace std;

struct Node {
    int data;
    int priority;
    int isActive; 
    Node* next;
};

class CircularPriorityQueue {
private:
    Node* front;
    Node* rear;
    unordered_map<int, Node*> nodeCache; // Cache to store pointers to nodes
    int maxSize; // Maximum size of the queue
    int currentSize; // Current number of active elements in the queue

public:
    CircularPriorityQueue(int size) {
        front = rear = nullptr;
        maxSize = size;
        currentSize = 0;
    }

    ~CircularPriorityQueue() {
        while (front != nullptr) {
            dequeue();
        }
    }

    void enqueue(int data, int priority, int isActive = 1) {
        if (currentSize >= maxSize) {
            cout << "Queue is full" << endl;
            return;
        }

        Node* temp = nullptr;
        // Check for inactive nodes to reuse
        Node* start = front;
        do {
            if (start != nullptr && start->isActive == 0) {
                temp = start;
                break;
            }
            start = start->next;
        } while (start != front);

        if (temp != nullptr) {
            // Reuse the inactive node
            temp->data = data;
            temp->priority = priority;
            temp->isActive = isActive;
        } else {
            // Create a new node
            temp = new Node();
            temp->data = data;
            temp->priority = priority;
            temp->isActive = isActive; 
            temp->next = nullptr;

            if (front == nullptr) {
                front = rear = temp;
                rear->next = front;
            } else {
                start = front;

                if (front->priority > priority) {
                    while (rear->next != front) {
                        rear = rear->next;
                    }
                    temp->next = front;
                    front = temp;
                    rear->next = front;
                } else {
                    while (start->next != front && start->next->priority <= priority) {
                        start = start->next;
                    }
                    temp->next = start->next;
                    start->next = temp;

                    if (start == rear) {
                        rear = temp;
                    }
                }
            }

            // Add the new node to the cache
            nodeCache[data] = temp;
        }

        currentSize++;
    }

    void dequeue() {
        if (front == nullptr) {
            cout << "Queue is empty" << endl;
            return;
        }

        Node* temp = front;
        Node* prev = rear;

        do {
            if (temp->isActive == 1) {
                if (temp == front) {
                    if (front == rear) {
                        nodeCache.erase(front->data); // Remove from cache
                        delete front;
                        front = rear = nullptr;
                    } else {
                        front = front->next;
                        rear->next = front;
                        nodeCache.erase(temp->data); // Remove from cache
                        delete temp;
                    }
                } else {
                    prev->next = temp->next;
                    if (temp == rear) {
                        rear = prev;
                    }
                    nodeCache.erase(temp->data); // Remove from cache
                    delete temp;
                }
                currentSize--;
                return;
            }
            prev = temp;
            temp = temp->next;
        } while (temp != front);

        cout << "No active elements to dequeue" << endl;
    }

    void display() {
        if (front == nullptr) {
            cout << "Queue is empty" << endl;
            return;
        }

        Node* temp = front;
        do {
            if (temp->isActive == 1) {
                cout << "Data: " << temp->data << " Priority: " << temp->priority << endl;
            }
            temp = temp->next;
        } while (temp != front);
    }

    void changeState(int data, int newState) {
        if (nodeCache.find(data) != nodeCache.end()) {
            Node* node = nodeCache[data];
            if (node->isActive != newState) {
                if (newState == 1) {
                    currentSize++;
                } else {
                    currentSize--;
                }
                node->isActive = newState;
            }
        } else {
            cout << "Node with data " << data << " not found" << endl;
        }
    }

    void pop() {
        if (front == nullptr) {
            cout << "Queue is empty" << endl;
            return;
        }

        cout << "Popping node with Data: " << front->data << " Priority: " << front->priority << endl;
        dequeue();
    }
};

int main() {
    CircularPriorityQueue queue(3); // Define the maximum size of the queue
    queue.enqueue(1, 1);
    queue.enqueue(2, 2);
    queue.enqueue(3, 3);

    cout << "Initial queue:" << endl;
    queue.display();

    cout << "Trying to enqueue another element (should fail):" << endl;
    queue.enqueue(4, 4); // This should print "Queue is full"

    cout << "Changing state of node with data 2 to inactive:" << endl;
    queue.changeState(2, 0);
    queue.display();

    cout << "Popping the current head node:" << endl;
    queue.pop();
    queue.display();

    cout << "Enqueuing a new element (should succeed):" << endl;
    queue.enqueue(4, 4); // This should succeed as there is an inactive node
    queue.display();

    return 0;
}