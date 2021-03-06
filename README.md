# 2η υποχρεωτική εργασία 2021


### Install

This project requires **Python** and the following Python libraries installed:

- [Pymongo]
- [Flask]
- [json]
- [uuid]
- [time]
- [bson.json_util]
- [bson import ObjectId]


### Τρόπος Λειτουργίας

- Δημιουργία ενός docker image που συνδέεται με ένα container της MongoDB , εισαγωγή της βάσης δεδομένων DSMarkets που περιέχει τα collections "Users" , "Products" στο image.
- Εκκίνηση του Docker Image , εισαγωγή του κώδικα στο Visual Studio Code με την ονομασία app.py εκκίνηση του κώδικα με την επιλογή Flask.
- Για την δοκιμή ανοίγουμε το postman και δημιουργούμε το request που επιθυμούμε να δοκιμάσουμε εισάγοντας στο url http://127.0.0.1:5000/ + το @app route του function. πχ. για το login http://127.0.0.1:5000/login έπειτα πατώντας body εισάγουμε στην επιλογή raw τις πληροφορίες σε μορφή json.![image](https://user-images.githubusercontent.com/62759358/122769937-aab38900-d2ad-11eb-8599-a9927447dd6b.png)


### Κώδικας 

Σε όλα τα function εκτός του create_user():, γίνεται έλεγχος του uuid του χρήστη η συγκεκριμένη υλοποίηση έχει γίνει χωρίς να χρειάζεται να εισάγει ο χρήστης κάπου το uuid γίνεται αυτόματα, επίσης οπού χρειάζεται ο χρήστης να εισάγει πληροφορία γίνεται επαλήθευση εάν το αρχείο και η πληροφορία βρίσκονται στη σωστή μορφη.Επιπροσθετα έχει προσδεθεί σε κάθε function μια if οπού ελέγχει εάν η κατηγορία του χρήστη που έχει συνδεθεί έχει τη δικαιοδοσία να χρησιμοποιήσει τη συγκεκριμένη λειτουργία.

# Extra Function για τον υπολογισμό της αξίας του καλαθιού του χρήστη - def get_cart_items_and_total_value(cart):

Το συγκεκριμένο function έχει δημιουργηθεί με σκοπό να υπολογίζει την αξία καλαθιού του χρήστη αλλά και να επιστρέφει και τα αντικείμενα μαζί με τις ποσότητες που βρίσκονται μέσα στο καλάθι. Το function δέχεται σαν όρισμα μόνο το καλάθι του χρήστη και επιστρέφει δυο μεταβλητές την items οπού περιέχει την ποσότητα και το όνομα κάθε αντικειμένου. Και την total_value που υπολογίζει την αξία. Ξεκινώντας το function δημιουργεί εάν πίνακα items και ορίζει το total_value = 0. Εν συνέχεια μέσω μιας for παίρνει κάθε key-value που περιέχει το καλάθι υστέρα κάνει αναζήτηση του αντικειμένου με το συγκεκριμένο key (το καλάθι έχει key το objectID και value τη ποσότητα του αντικειμένου) εισαγει το ονομα του σε μια μεταβλητή item_name, ενημερώνει το total_value με τον πολλαπλασιασμό της τιμής και της ποσότητας + το total_value και εισάγει στο πίνακα items το string ποσότητα of item_name. Όταν ολοκληρωθεί η διαδικασία επιστρέφεται ο πίνακας μαζί με το total_value


# Function 1: Δημιουργία χρήστη - def create_user():
 
Έλεγχος αν το email υπάρχει ήδη μέσα στη βάση δεδομένων. Εφόσον δεν υπάρχει γίνεται εισαγωγή των στοιχείων του νέου χρήστη στη βάση δεδομένων μας.


# Function 2: Login στο σύστημα - def login():

Έλεγχος αν το email υπάρχει ήδη μέσα στη βάση δεδομένων. Εφόσον υπάρχει βρίσκουμε το password που του αντιστοιχεί και το αποθηκεύουμε σε μια νέα μεταβλητή , υστέρα κάνουμε έλεγχο αν το ζεύγος που λάβαμε ως εισαγωγή είναι το ίδιο με το ζεύγος που υπάρχει μέσα στη βάση δεδομένων μας. Έπειτα δημιουργούμε το uuid  που αντιστοιχεί στο email του χρήστη. Επίσης δημιουργούμε δυο global μεταβλητές που αποθηκεύουμε το email και την κατηγορία του χρήστη.


# Function 3: Διαγραφή του χρήστη από το σύστημα - def deleteUser():

διαγραφή του χρήστη από την βάση δεδομένων.

# Function 4: Εισαγωγή αντικειμένου στη βάση δεδομένων των προϊόντων - def insertItem():

Στο συγκεκριμένο function δεχόμαστε σαν εισαγωγή όλες τις πληροφορίες του αντικειμένου και μόνο εφόσον υπάρχουν όλες στη σωστή μορφή η διαδικασία συνεχίζει, εφόσον όλα τα στοιχεία είναι σωστά τα προσθέτουμε σε μια καινούργια μεταβλητή product και υστέρα εισάγουμε την μεταβλητή στη βάση δεδομένων Products.

# Function 5: Διαγραφή αντικειμένου από την βάση δεδομένων των προϊόντων - def DeleteItem():
 
Στο συγκεκριμένο function δεχόμαστε σαν εισαγωγή το id του αντικειμένου και το διαγράφουμε από την βάση δεδομένων Products.

# Function 6: Ενημέρωση αντικειμένου από την βάση δεδομένων των προϊόντων - def UpdateItem():

Στο συγκεκριμένο function δεχόμαστε σαν εισαγωγή το id του αντικειμένου και εάν η περισσότερα από τα χαρακτηριστικά του που θέλουμε να ενημερώσουμε , εφόσον δεχθούμε πληροφορία για εάν η περισσότερα χαρακτηριστικά του ενημερώνουμε το προϊόν .

# Function 7: Αναζήτηση αντικειμένου από την βάση δεδομένων των προϊόντων - def search():

Στο συγκεκριμένο function δεχόμαστε σαν εισαγωγή μια από όλες τις πληροφορίες του αντικειμένου εάν βρεθεί εάν η περισσότερα αντικείμενα τα επιστρέφουμε αλλιώς επιστρέφουμε ότι δε βρέθηκε αποτέλεσμα.

# Function 8: Εισαγωγή αντικειμένου στο καλάθι του χρήστη - def addItem():

Στο συγκεκριμένο function δεχόμαστε σαν εισαγωγή το id και την ποσότητα την οποία θέλει να προσθέσει στο καλάθι του ο χρήστης. Εάν δε βρεθεί αντικείμενο επιστρέφετε κατάλληλο μήνυμα αλλιώς γίνεται έλεγχος εάν υπάρχει διαθέσιμη η ποσότητα που θέλει να προσθέσει ο χρήστης στο καλάθι του εάν δεν υπάρχει διαθέσιμη ποσότητα επιστρέφετε μήνυμα με τη διαθέσιμη ποσότητα για το συγκεκριμένο αντικείμενο. Αν υπάρχει η ποσότητα που θέλει να προσθέσει ο χρήστης στο καλάθι του γίνεται δέσμευση της ποσότητας που προσδέθηκε στο καλάθι του χρήστη. Υστέρα δημιουργείται μια global μεταβλητή cart με key το id του αντικειμένου οπού έχει σαν εισαγωγή τη ποσότητα του αντικειμένου. Έπειτα τα δεδομένα μεταφέρονται στο function get_cart_items_and_total_value() οπού γίνεται ο υπολογισμός της αξίας του καλαθιού.

# Function 9: Εμφάνιση του καλαθιού του χρήση - def showCart():

Στο συγκεκριμένο function παίρνουμε την global μεταβλητή cart αν είναι None επιστρέφουμε ότι το καλάθι είναι άδειο αλλιώς καλούμε πάλι το function get_cart_items_and_total_value() οπού γίνεται ο υπολογισμός της αξίας του καλαθιού μαζί με τα αντικείμενα που έχει μέσα.

# Function 10: Διαγραφή αντικειμένου από το καλάθι του χρήστη - def deleteFromCart()

Στο συγκεκριμένο function δεχόμαστε το id του αντικειμένου που θέλει να διαγράψει από το καλάθι του ο χρήστης και παίρνουμε και την global μεταβλητή cart. Δημιουργούμε μια προϋπόθεση Try - except . Στο try δημιουργούμε εάν dictionary delete και εισάγουμε μέσα τα δεδομένα του cart[id] έπειτα κάνουμε διαγραφή από το καλάθι του χρήστη το cart[id] μέσω του except Key Error as ex: εάν δεν υπάρχει το συγκεκριμένο αντικείμενο στα καλάθι εμφανίζεται κατάλληλο μήνυμα λάθους. Εάν υπάρχει συνεχίζουμε ενημερώνοντας το stock του προϊόντος προσθέτοντας την ποσότητα που είχε προσθέσει ο χρήστης στο καλάθι του. Τέλος εμφανίζουμε το ανανεωμένο του καλάθι.

# Function 11: Αγορά των προϊόντων που βρίσκονται στο καλάθι του χρήστη - def Purchase(): 

Στο συγκεκριμένο function δεχόμαστε την κάρτα του χρήστη, και παίρνουμε την global μεταβλητή cart αν η μεταβλητή cart είναι άδεια εμφανίζουμε μήνυμα ότι το καλάθι είναι άδειο αλλιώς ελέγχουμε εάν η κάρτα αποτελείται από 16 ψηφιά εάν δεν αποτελείται από 16 ψηφιά εμφανίζουμε μήνυμα λάθους αλλιώς συνεχίζουμε κάνοντας αναζήτηση του χρήστη στη βάση μέσω της global μεταβλητής user_email καλώντας την συνάρτηση  cart_items, total_value = get_cart_items_and_total_value(cart) παίρνουμε τα δεδομένα του καλαθιού του χρήστη και τα αποθηκεύουμε σε μια μεταβλητή order. Ύστερα κάνουμε έλεγχο εάν ο χρήστης έχει ξαναπαραγγειλει εάν όχι τότε δημιουργούμε το ιστορικό παραγγελιών του χρήστη και περνάμε μέσα την παραγγελία που μόλις έκανε. Εφόσον δεν είναι η πρώτη παραγγελία του χρήστη τότε δημιουργούμε μια καινούργια μεταβλητή την order_History και περνάμε μέσα το ιστορικό του από τη βάση υστέρα κάνουμε εάν for loop σε όλο του το ιστορικό για να βρούμε ποιο είναι το τελευταίο key ώστε να περάσουμε την καινούρια παραγγελία στο άμεσος επόμενο του. Όταν ολοκληρωθεί η διαδικασία ενημερώνουμε το ιστορικό του χρήστη, αδειάζουμε το καλάθι του και του εμφανίζουμε την απόδειξη της παραγγελίας του.

# Function 12: Εμφάνιση των προηγουμένων παραγγελιών του χρήστη - def orderHistory():

Στο συγκεκριμένο function παίρνουμε την global μεταβλητή user_email και κάνουμε αναζήτηση του χρήστη στη βάση δεδομένων υστέρα ελέγχουμε εάν υπάρχει ιστορικό παραγγελιών για τον χρήστη εάν δεν υπάρχει επιστρέφεται κατάλληλο μήνυμα αλλιώς επιστρέφεται το ιστορικό των παραγγελιών του.
