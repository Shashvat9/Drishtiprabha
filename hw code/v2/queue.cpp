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

public:
    CircularPriorityQueue() {
        front = rear = nullptr;
    }

    ~CircularPriorityQueue() {
        while (front != nullptr) {
            dequeue();
        }
    }

    void enqueue(int data, int priority, int isActive = 1) {
        Node* temp = new Node();
        temp->data = data;
        temp->priority = priority;
        temp->isActive = isActive; 
        temp->next = nullptr;

        if (front == nullptr) {
            front = rear = temp;
            rear->next = front;
        } else {
            Node* start = front;

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
            nodeCache[data]->isActive = newState;
        } else {
            cout << "Node with data " << data << " not found" << endl;
        }
    }
};

int main() {
    CircularPriorityQueue queue;
    queue.enqueue(1, 1);
    queue.enqueue(2, 2);
    queue.enqueue(3, 3);

    cout << "Initial queue:" << endl;
    queue.display();

    cout << "Changing state of node with data 2 to inactive:" << endl;
    queue.changeState(2, 0);
    queue.display();

    cout << "Dequeueing an active element:" << endl;
    queue.dequeue();
    queue.display();

    return 0;
}