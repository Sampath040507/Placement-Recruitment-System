class Candidate:
    def _init_(self, id, name, gpa, experience, skills, coding_marks):
        self.id = id
        self.name = name
        self.gpa = gpa
        self.experience = experience
        self.skills = skills
        self.coding_marks = coding_marks

class ListNode:
    def _init_(self, candidate):
        self.candidate = candidate
        self.next = None

class LinkedList:
    def _init_(self):
        self.head = None

    def insert(self, candidate):
        new_node = ListNode(candidate)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = new_node

    def _iter_(self):
        current = self.head
        while current:
            yield current.candidate
            current = current.next

class BSTNode:
    def _init_(self, gpa):
        self.gpa = gpa
        self.linked_list = LinkedList()
        self.left = None
        self.right = None

class BST:
    def _init_(self):
        self.root = None

    def insert(self, candidate):
        if self.root is None:
            self.root = BSTNode(candidate.gpa)
            self.root.linked_list.insert(candidate)
        else:
            self._insert(self.root, candidate)

    def _insert(self, node, candidate):
        if candidate.gpa < node.gpa:
            if node.left is None:
                node.left = BSTNode(candidate.gpa)
                node.left.linked_list.insert(candidate)
            else:
                self._insert(node.left, candidate)
        elif candidate.gpa > node.gpa:
            if node.right is None:
                node.right = BSTNode(candidate.gpa)
                node.right.linked_list.insert(candidate)
            else:
                self._insert(node.right, candidate)
        else:
            node.linked_list.insert(candidate)

    def search(self, gpa):
        return self._search(self.root, gpa)

    def _search(self, node, gpa):
        if node is None or node.gpa == gpa:
            return node
        if gpa < node.gpa:
            return self._search(node.left, gpa)
        return self._search(node.right, gpa)

    def in_order_traversal(self):
        nodes = []
        self._in_order_traversal(self.root, nodes)
        return nodes

    def _in_order_traversal(self, node, nodes):
        if node:
            self._in_order_traversal(node.left, nodes)
            nodes.append(node)
            self._in_order_traversal(node.right, nodes)

class InterviewSlot:
    def _init_(self, time, candidate=None):
        self.time = time
        self.candidate = candidate

class Scheduler:
    def _init_(self):
        self.slots = []

    def add_slot(self, time):
        self.slots.append(InterviewSlot(time))

    def schedule_candidate(self, time, candidate):
        for slot in self.slots:
            if slot.time == time and slot.candidate is None:
                slot.candidate = candidate
                return True
        return False

    def get_schedule(self):
        return [(slot.time, slot.candidate.name if slot.candidate else "Free") for slot in self.slots]

class CandidateSelectionSystem:
    def _init_(self):
        self.bst = BST()
        self.scheduler = Scheduler()
        self.hash_table = {}

    def add_candidate(self, candidate):
        self.bst.insert(candidate)
        self.hash_table[candidate.id] = candidate

    def search_candidate_by_id(self, candidate_id):
        return self.hash_table.get(candidate_id, None)

    def search_candidate_by_gpa(self, gpa):
        node = self.bst.search(gpa)
        if node:
            return list(node.linked_list)
        return []

    def sort_candidates_by_gpa(self):
        nodes = self.bst.in_order_traversal()
        sorted_candidates = []
        for node in nodes:
            for candidate in node.linked_list:
                sorted_candidates.append(candidate)
        return sorted_candidates

    def shortlist_candidates(self, min_gpa, required_skills, min_experience, min_coding_marks):
        shortlisted = []
        nodes = self.bst.in_order_traversal()
        for node in nodes:
            if node.gpa >= min_gpa:
                for candidate in node.linked_list:
                    if (candidate.experience >= min_experience and
                        candidate.coding_marks >= min_coding_marks and
                        all(skill in candidate.skills for skill in required_skills)):
                        shortlisted.append(candidate)
        return shortlisted

    def filter_candidates_by_coding_marks(self, min_marks):
        filtered = []
        for candidate in self.hash_table.values():
            if candidate.coding_marks >= min_marks:
                filtered.append(candidate)
        return filtered

    def generate_report(self):
        report = {}
        report['total_candidates'] = len(self.hash_table)
        report['shortlisted_candidates'] = len(self.shortlist_candidates(3.5, ['Python', 'Data Structures'], 2, 75))
        report['all_candidates'] = [(candidate.id, candidate.name, candidate.gpa, candidate.experience, candidate.skills, candidate.coding_marks) for candidate in self.hash_table.values()]
        return report

def main():
    system = CandidateSelectionSystem()
    
    while True:
        print("\nCandidate Selection System Menu")
        print("1. Add Candidate")
        print("2. Search Candidate by ID")
        print("3. Search Candidate by GPA")
        print("4. Sort Candidates by GPA")
        print("5. Shortlist Candidates")
        print("6. Filter Candidates by Coding Test Marks")
        print("7. Schedule Interview")
        print("8. View Schedule")
        print("9. Generate All Candidate Details")
        print("10. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            id = int(input("Enter ID: "))
            name = input("Enter Name: ")
            gpa = float(input("Enter GPA: "))
            experience = int(input("Enter Experience (in years): "))
            skills = input("Enter Skills (comma separated): ").split(",")
            coding_marks = float(input("Enter marks in coding test: "))
            candidate = Candidate(id, name, gpa, experience, skills, coding_marks)
            system.add_candidate(candidate)
            print(f"Candidate {name} added successfully.")

        elif choice == "2":
            id = int(input("Enter ID: "))
            candidate = system.search_candidate_by_id(id)
            if candidate:
                print(f"ID: {candidate.id}, Name: {candidate.name}, GPA: {candidate.gpa}, Experience: {candidate.experience}, Skills: {', '.join(candidate.skills)}, Coding Marks: {candidate.coding_marks}")
            else:
                print("Candidate not found.")

        elif choice == "3":
            gpa = float(input("Enter GPA: "))
            candidates = system.search_candidate_by_gpa(gpa)
            if candidates:
                for candidate in candidates:
                    print(f"ID: {candidate.id}, Name: {candidate.name}, GPA: {candidate.gpa}, Experience: {candidate.experience}, Skills: {', '.join(candidate.skills)}, Coding Marks: {candidate.coding_marks}")
            else:
                print("No candidates found with the specified GPA.")

        elif choice == "4":
            candidates = system.sort_candidates_by_gpa()
            print("Candidates sorted by GPA:")
            for candidate in candidates:
                print(f"GPA: {candidate.gpa}, ID: {candidate.id}, Name: {candidate.name}")

        elif choice == "5":
            min_gpa = float(input("Enter minimum GPA: "))
            required_skills = input("Enter required skills (comma separated): ").split(",")
            min_experience = int(input("Enter minimum experience (in years): "))
            min_coding_marks = float(input("Enter minimum coding test marks: "))
            shortlisted = system.shortlist_candidates(min_gpa, required_skills, min_experience, min_coding_marks)
            if shortlisted:
                print(f"*Shortlisted candidates with min GPA {min_gpa}, skills {required_skills}, min experience {min_experience}, and min coding test marks {min_coding_marks}*:")
                for candidate in shortlisted:
                    print(f"ID: {candidate.id}, Name: {candidate.name}, GPA: {candidate.gpa}, Experience: {candidate.experience}, Skills: {', '.join(candidate.skills)}, Coding Marks: {candidate.coding_marks}")
            else:
                print("No candidates matched the criteria.")

        elif choice == "6":
            min_marks = float(input("Enter minimum marks in coding test: "))
            filtered = system.filter_candidates_by_coding_marks(min_marks)
            if filtered:
                print(f"Candidates with coding test marks >= {min_marks}:")
                for candidate in filtered:
                    print(f"ID: {candidate.id}, Name: {candidate.name}, GPA: {candidate.gpa}, Experience: {candidate.experience}, Skills: {', '.join(candidate.skills)}, Coding Marks: {candidate.coding_marks}")
            else:
                print("No candidates found with the specified coding test marks.")

        elif choice == "7":
            time = input("Enter interview time (e.g., '10:00 AM'): ")
            id = int(input("Enter candidate ID: "))
            system.scheduler.add_slot(time)
            candidate = system.search_candidate_by_id(id)
            if candidate:
                if system.scheduler.schedule_candidate(time, candidate):
                    print(f"Candidate {candidate.name} scheduled for interview at {time}.")
                else:
                    print("Slot already taken or not available.")
            else:
                print("Candidate not found.")

        elif choice == "8":
            schedule = system.scheduler.get_schedule()
            print("Interview Schedule:")
            for time, candidate_name in schedule:
                print(f"Time: {time}, Candidate: {candidate_name}")

        elif choice == "9":
            report = system.generate_report()
            print("\nReport:")
            print(f"Total candidates: {report['total_candidates']}")
            print(f"Shortlisted candidates: {report['shortlisted_candidates']}")
            print("Details of all candidates:")
            for candidate in report['all_candidates']:
                print(f"ID: {candidate[0]}, Name: {candidate[1]}, GPA: {candidate[2]}, Experience: {candidate[3]}, Skills: {', '.join(candidate[4])}, Coding Marks: {candidate[5]}")

        elif choice == "10":
            print("Exiting the system.")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "_main_":
    main()