-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 19, 2026 at 05:25 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `edubot_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `admins`
--

CREATE TABLE `admins` (
  `admin_id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admins`
--

INSERT INTO `admins` (`admin_id`, `name`, `email`, `password_hash`, `created_at`) VALUES
(1, 'pranjal', 'admin@edubot.com', 'pbkdf2:sha256:260000$test$9a5d7b6b9b8c8bdf8e5b5cbe5c9c3f8f9b8a2bfa7fef6a8cbd', '2026-02-06 13:55:33');

-- --------------------------------------------------------

--
-- Table structure for table `flashcards`
--

CREATE TABLE `flashcards` (
  `flashcard_id` bigint(20) UNSIGNED NOT NULL,
  `topic` varchar(100) DEFAULT NULL,
  `content` text NOT NULL,
  `created_by` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `flashcards`
--

INSERT INTO `flashcards` (`flashcard_id`, `topic`, `content`, `created_by`) VALUES
(1, 'OOP in Java', 'Q: Name any one OOP concept used in Java.\nA: Inheritance.', 1),
(2, 'Java Basics', 'Q: Why is Java platform independent?\nA: Because Java code runs on JVM, not directly on OS.', 1),
(3, 'OOP in Java', 'Q: What is a class?\nA: A blueprint for creating objects.', 1),
(4, 'Java Basics', 'Q: What is JVM?\nA: JVM stands for Java Virtual Machine. It runs Java bytecode and makes Java platform independent.', 1),
(5, 'Java Basics', 'Q: What is JDK?\nA: JDK stands for Java Development Kit. It contains compiler and tools required to develop Java programs.', 1),
(6, 'Java Basics', 'Q: What is JRE?\nA: JRE stands for Java Runtime Environment. It is used to run Java applications.', 1),
(7, 'OOP in Java', 'Q: What is Encapsulation?\nA: Encapsulation is wrapping data and methods together inside a class.', 1),
(8, 'OOP in Java', 'Q: What is Inheritance?\nA: Inheritance allows one class to acquire properties of another class.', 1),
(9, 'OOP in Java', 'Q: What is Polymorphism?\nA: Polymorphism means many forms. It allows methods to behave differently.', 1),
(10, 'OOP in Java', 'Q: What is Abstraction?\nA: Abstraction hides implementation details and shows only essential features.', 1),
(11, 'Java Collections', 'Q: What is ArrayList?\nA: ArrayList is a resizable array implementation in Java.', 1),
(12, 'Java Collections', 'Q: What is HashMap?\nA: HashMap stores data in key-value pairs.', 1),
(13, 'Exception Handling', 'Q: What is Exception?\nA: Exception is an event that disrupts normal program flow.', 1),
(14, 'Exception Handling', 'Q: What is try-catch block?\nA: It is used to handle exceptions in Java.', 1),
(15, 'Python Basics', 'Q: What is Python?\nA: Python is a high-level, interpreted programming language.', 1),
(16, 'Python Basics', 'Q: What is a list in Python?\nA: A list is a mutable sequence of elements enclosed in square brackets.', 1),
(17, 'Python Basics', 'Q: What is a tuple?\nA: A tuple is an immutable sequence of elements.', 1),
(18, 'Python OOP', 'Q: How do you define a class in Python?\nA: Using the class keyword.', 1),
(19, 'Python OOP', 'Q: What is __init__ method?\nA: It is a constructor method that initializes object attributes.', 1),
(20, 'File Handling', 'Q: How to open a file in Python?\nA: Using open() function with mode like \"r\" or \"w\".', 1);

-- --------------------------------------------------------

--
-- Table structure for table `flashcard_activity`
--

CREATE TABLE `flashcard_activity` (
  `activity_id` int(11) NOT NULL,
  `student_id` int(11) NOT NULL,
  `flashcard_id` bigint(20) UNSIGNED NOT NULL,
  `viewed_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `flashcard_activity`
--

INSERT INTO `flashcard_activity` (`activity_id`, `student_id`, `flashcard_id`, `viewed_at`) VALUES
(1, 1, 1, '2026-02-11 05:47:21'),
(2, 1, 1, '2026-02-11 05:48:04'),
(3, 1, 1, '2026-02-11 05:54:56'),
(4, 1, 1, '2026-02-11 05:59:22'),
(5, 1, 2, '2026-02-11 05:59:22'),
(6, 1, 3, '2026-02-11 05:59:22');

-- --------------------------------------------------------

--
-- Table structure for table `programs`
--

CREATE TABLE `programs` (
  `program_id` bigint(20) UNSIGNED NOT NULL,
  `title` varchar(150) NOT NULL,
  `language` varchar(50) NOT NULL,
  `topic` varchar(100) DEFAULT NULL,
  `keywords` text DEFAULT NULL,
  `code_snippet` text NOT NULL,
  `created_by` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `programs`
--

INSERT INTO `programs` (`program_id`, `title`, `language`, `topic`, `keywords`, `code_snippet`, `created_by`) VALUES
(1, 'Sum of Two Numbers', 'Java', 'Operators', 'java, addition, operators', 'import java.util.Scanner;\r\n     class Sum {\r\n        public static void main(String[] args) {\r\n            Scanner sc = new Scanner(System.in);\r\n            int a = sc.nextInt();\r\n            int b = sc.nextInt();\r\n            System.out.println(a + b);\r\n        }\r\n     }', 1),
(2, 'Factorial Program', 'Java', 'Loops', 'java, factorial, loops', 'class Factorial {\r\n        static int fact(int n) {\r\n            if(n == 0) return 1;\r\n            return n * fact(n-1);\r\n        }\r\n        public static void main(String[] args) {\r\n            System.out.println(fact(5));\r\n        }\r\n    }', 1),
(3, 'Sum of Two Numbers', 'Java', 'Operators', 'java, addition, operators', 'public class Sum {\r\n    public static void main(String[] args) {\r\n        int a = 10, b = 20;\r\n        System.out.println(a + b);\r\n    }\r\n}', 1),
(4, 'Even or Odd', 'Java', 'Conditionals', 'java, even odd, if else', 'public class EvenOdd {\r\n    public static void main(String[] args) {\r\n        int n = 7;\r\n        if(n % 2 == 0)\r\n            System.out.println(\"Even\");\r\n        else\r\n            System.out.println(\"Odd\");\r\n    }\r\n}', 1),
(5, 'Factorial using Loop', 'Java', 'Loops', 'java, factorial, loops', 'public class Factorial {\r\n    public static void main(String[] args) {\r\n        int n = 5, fact = 1;\r\n        for(int i=1;i<=n;i++)\r\n            fact *= i;\r\n        System.out.println(fact);\r\n    }\r\n}', 1),
(6, 'Fibonacci Series', 'Java', 'Loops', 'java, fibonacci', 'public class Fibonacci {\r\n    public static void main(String[] args) {\r\n        int a=0,b=1,c;\r\n        for(int i=0;i<10;i++){\r\n            System.out.print(a+\" \");\r\n            c=a+b; a=b; b=c;\r\n        }\r\n    }\r\n}', 1),
(7, 'Prime Number Check', 'Java', 'Loops', 'java, prime number', 'public class Prime {\r\n    public static void main(String[] args) {\r\n        int n=7, flag=0;\r\n        for(int i=2;i<=n/2;i++){\r\n            if(n%i==0){ flag=1; break; }\r\n        }\r\n        if(flag==0) System.out.println(\"Prime\");\r\n        else System.out.println(\"Not Prime\");\r\n    }\r\n}', 1),
(8, 'Palindrome String', 'Java', 'Strings', 'java, palindrome, string', 'public class Palindrome {\r\n    public static void main(String[] args) {\r\n        String s=\"madam\", rev=\"\";\r\n        for(int i=s.length()-1;i>=0;i--)\r\n            rev+=s.charAt(i);\r\n        System.out.println(s.equals(rev));\r\n    }\r\n}', 1),
(9, 'Reverse Number', 'Java', 'Loops', 'java, reverse number', 'public class ReverseNum {\r\n    public static void main(String[] args) {\r\n        int n=123, rev=0;\r\n        while(n>0){\r\n            rev=rev*10+n%10;\r\n            n/=10;\r\n        }\r\n        System.out.println(rev);\r\n    }\r\n}', 1),
(10, 'Swap Two Numbers', 'Java', 'Operators', 'java, swap', 'public class Swap {\r\n    public static void main(String[] args) {\r\n        int a=5,b=10,temp;\r\n        temp=a; a=b; b=temp;\r\n        System.out.println(a+\" \"+b);\r\n    }\r\n}', 1),
(11, 'Largest of Three', 'Java', 'Conditionals', 'java, largest', 'public class Largest {\r\n    public static void main(String[] args) {\r\n        int a=10,b=20,c=15;\r\n        int max = (a>b)?a:b;\r\n        max = (max>c)?max:c;\r\n        System.out.println(max);\r\n    }\r\n}', 1),
(12, 'Array Sum', 'Java', 'Arrays', 'java, array sum', 'public class ArraySum {\r\n    public static void main(String[] args) {\r\n        int[] arr={1,2,3,4};\r\n        int sum=0;\r\n        for(int i:arr) sum+=i;\r\n        System.out.println(sum);\r\n    }\r\n}', 1),
(13, 'Linear Search', 'Java', 'Arrays', 'java, linear search', 'public class LinearSearch {\r\n    public static void main(String[] args) {\r\n        int[] arr={1,2,3,4};\r\n        int key=3;\r\n        for(int i=0;i<arr.length;i++)\r\n            if(arr[i]==key) System.out.println(\"Found\");\r\n    }\r\n}', 1),
(14, 'Bubble Sort', 'Java', 'Arrays', 'java, bubble sort', 'public class BubbleSort {\r\n    public static void main(String[] args) {\r\n        int[] arr={5,2,4,1};\r\n        for(int i=0;i<arr.length;i++)\r\n            for(int j=0;j<arr.length-1;j++)\r\n                if(arr[j]>arr[j+1]){\r\n                    int t=arr[j]; arr[j]=arr[j+1]; arr[j+1]=t;\r\n                }\r\n        for(int i:arr) System.out.print(i+\" \");\r\n    }\r\n}', 1),
(15, 'Class and Object Example', 'Java', 'OOP', 'java, class object', 'class Student {\r\n    int id; String name;\r\n    public static void main(String[] args){\r\n        Student s=new Student();\r\n        s.id=1; s.name=\"John\";\r\n        System.out.println(s.id+\" \"+s.name);\r\n    }\r\n}', 1),
(16, 'Constructor Example', 'Java', 'OOP', 'java, constructor', 'class Demo {\r\n    Demo(){ System.out.println(\"Constructor called\"); }\r\n    public static void main(String[] args){\r\n        Demo d=new Demo();\r\n    }\r\n}', 1),
(17, 'Method Overloading', 'Java', 'OOP', 'java, overloading', 'class Overload {\r\n    int add(int a,int b){ return a+b; }\r\n    double add(double a,double b){ return a+b; }\r\n    public static void main(String[] args){\r\n        Overload o=new Overload();\r\n        System.out.println(o.add(2,3));\r\n    }\r\n}', 1),
(18, 'Inheritance Example', 'Java', 'OOP', 'java, inheritance', 'class A { void show(){ System.out.println(\"Parent\"); } }\r\nclass B extends A {\r\n    public static void main(String[] args){\r\n        B obj=new B();\r\n        obj.show();\r\n    }\r\n}', 1),
(19, 'Interface Example', 'Java', 'OOP', 'java, interface', 'interface DemoInt {\r\n    void show();\r\n}\r\nclass Test implements DemoInt{\r\n    public void show(){ System.out.println(\"Interface\"); }\r\n    public static void main(String[] args){\r\n        Test t=new Test();\r\n        t.show();\r\n    }\r\n}', 1),
(20, 'Exception Handling', 'Java', 'Exception', 'java, exception', 'public class ExceptionDemo {\r\n    public static void main(String[] args){\r\n        try{\r\n            int a=10/0;\r\n        }catch(Exception e){\r\n            System.out.println(\"Error\");\r\n        }\r\n    }\r\n}', 1),
(21, 'File Writing', 'Java', 'File Handling', 'java, file', 'import java.io.*;\r\npublic class FileWrite {\r\n    public static void main(String[] args)throws Exception{\r\n        FileWriter fw=new FileWriter(\"test.txt\");\r\n        fw.write(\"Hello\");\r\n        fw.close();\r\n    }\r\n}', 1),
(22, 'HashMap Example', 'Java', 'Collections', 'java, hashmap', 'import java.util.*;\r\npublic class MapDemo{\r\n    public static void main(String[] args){\r\n        HashMap<Integer,String> map=new HashMap<>();\r\n        map.put(1,\"A\");\r\n        System.out.println(map.get(1));\r\n    }\r\n}', 1),
(23, 'ArrayList Example', 'Java', 'Collections', 'java, arraylist', 'import java.util.*;\r\npublic class ListDemo{\r\n    public static void main(String[] args){\r\n        ArrayList<Integer> list=new ArrayList<>();\r\n        list.add(10);\r\n        System.out.println(list);\r\n    }\r\n}', 1),
(24, 'String Length', 'Java', 'Strings', 'java, string length', 'public class StrLen{\r\n    public static void main(String[] args){\r\n        String s=\"Hello\";\r\n        System.out.println(s.length());\r\n    }\r\n}', 1),
(25, 'Armstrong Number', 'Java', 'Loops', 'java, armstrong', 'public class Armstrong{\r\n    public static void main(String[] args){\r\n        int n=153,sum=0,temp=n;\r\n        while(n>0){\r\n            int r=n%10;\r\n            sum+=r*r*r;\r\n            n/=10;\r\n        }\r\n        System.out.println(sum==temp);\r\n    }\r\n}', 1),
(26, 'Multiplication Table', 'Java', 'Loops', 'java, table', 'public class Table{\r\n    public static void main(String[] args){\r\n        for(int i=1;i<=10;i++)\r\n            System.out.println(5*i);\r\n    }\r\n}', 1),
(27, 'Count Vowels', 'Java', 'Strings', 'java, vowels', 'public class Vowels{\r\n    public static void main(String[] args){\r\n        String s=\"education\";\r\n        int count=0;\r\n        for(char c:s.toCharArray())\r\n            if(\"aeiou\".indexOf(c)!=-1) count++;\r\n        System.out.println(count);\r\n    }\r\n}', 1),
(28, 'Sum of Two Numbers', 'Python', 'Operators', 'python, addition', 'a=10\nb=20\nprint(a+b)', 1),
(29, 'Even or Odd', 'Python', 'Conditionals', 'python, even odd', 'n=7\nprint(\"Even\" if n%2==0 else \"Odd\")', 1),
(30, 'Factorial', 'Python', 'Loops', 'python, factorial', 'n=5\nfact=1\nfor i in range(1,n+1):\n    fact*=i\nprint(fact)', 1),
(31, 'Fibonacci', 'Python', 'Loops', 'python, fibonacci', 'a,b=0,1\nfor _ in range(10):\n    print(a,end=\" \")\n    a,b=b,a+b', 1),
(32, 'Prime Check', 'Python', 'Loops', 'python, prime', 'n=7\nflag=True\nfor i in range(2,n//2+1):\n    if n%i==0:\n        flag=False\nprint(flag)', 1),
(33, 'Palindrome String', 'Python', 'Strings', 'python, palindrome', 's=\"madam\"\nprint(s==s[::-1])', 1),
(34, 'List Sum', 'Python', 'Lists', 'python, list sum', 'arr=[1,2,3]\nprint(sum(arr))', 1),
(35, 'Dictionary Example', 'Python', 'Collections', 'python, dict', 'd={1:\"A\"}\nprint(d[1])', 1),
(36, 'Exception Handling', 'Python', 'Exception', 'python, try except', 'try:\n    print(10/0)\nexcept:\n    print(\"Error\")', 1),
(37, 'File Write', 'Python', 'File Handling', 'python, file', 'with open(\"test.txt\",\"w\") as f:\n    f.write(\"Hello\")', 1);

-- --------------------------------------------------------

--
-- Table structure for table `questions`
--

CREATE TABLE `questions` (
  `question_id` bigint(20) UNSIGNED NOT NULL,
  `quiz_id` int(11) NOT NULL,
  `question_text` text NOT NULL,
  `correct_option` varchar(50) NOT NULL,
  `option_a` varchar(255) NOT NULL,
  `option_b` varchar(255) NOT NULL,
  `option_c` varchar(255) NOT NULL,
  `option_d` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `questions`
--

INSERT INTO `questions` (`question_id`, `quiz_id`, `question_text`, `correct_option`, `option_a`, `option_b`, `option_c`, `option_d`) VALUES
(4, 1, 'Which keyword is used to create an object in Java?', 'B', 'class', 'new', 'this', 'static'),
(5, 1, 'Which method is the entry point of a Java program?', 'B', 'start()', 'main()', 'run()', 'init()'),
(6, 1, 'Which data type is used to store whole numbers?', 'C', 'float', 'double', 'int', 'char'),
(7, 1, 'Which keyword is used to declare a variable?', 'A', 'int', 'define', 'var', 'declare'),
(8, 1, 'Which operator is used for remainder?', 'C', '/', '*', '%', '+'),
(9, 1, 'Which of these is not a primitive data type?', 'D', 'int', 'float', 'boolean', 'String'),
(10, 1, 'Which loop is best when number of iterations is known?', 'B', 'while', 'for', 'do-while', 'foreach'),
(11, 1, 'Which keyword is used to exit a loop?', 'A', 'break', 'continue', 'exit', 'return'),
(12, 1, 'Which class is automatically imported?', 'C', 'java.util', 'java.io', 'java.lang', 'java.net'),
(13, 1, 'Boolean values in Java are?', 'D', '0 or 1', 'Yes or No', '1 or -1', 'true or false'),
(14, 2, 'What is abstraction?', 'B', 'Hiding data', 'Hiding implementation details', 'Overloading methods', 'Using static methods'),
(15, 2, 'Which keyword refers to current object?', 'A', 'this', 'super', 'self', 'current'),
(16, 2, 'Method overriding requires?', 'C', 'Same class', 'Static methods', 'Same method signature', 'Private methods'),
(17, 2, 'Which access modifier is most restrictive?', 'D', 'public', 'protected', 'default', 'private'),
(18, 2, 'ArrayList belongs to which package?', 'A', 'java.util', 'java.io', 'java.lang', 'java.net'),
(19, 2, 'Which block always executes?', 'B', 'try', 'finally', 'catch', 'throw'),
(20, 2, 'Which keyword is used to inherit interface?', 'C', 'extends', 'inherits', 'implements', 'uses'),
(21, 2, 'Polymorphism means?', 'A', 'Many forms', 'Many classes', 'Many variables', 'Many loops'),
(22, 2, 'Which collection allows duplicates?', 'B', 'Set', 'List', 'Map', 'Queue'),
(23, 2, 'Garbage collection is handled by?', 'D', 'Programmer', 'Compiler', 'OS', 'JVM'),
(24, 3, 'Which keyword creates a class?', 'C', 'define', 'object', 'class', 'struct'),
(25, 3, 'Which data type is immutable?', 'A', 'tuple', 'list', 'dict', 'set'),
(26, 3, 'Indentation in Python is?', 'B', 'Optional', 'Mandatory', 'Ignored', 'Deprecated'),
(27, 3, 'Which function prints output?', 'D', 'echo()', 'display()', 'write()', 'print()'),
(28, 3, 'Which operator checks equality?', 'A', '==', '=', '!=', '<>'),
(29, 3, 'Which keyword is used for loop control skip?', 'C', 'break', 'exit', 'continue', 'stop'),
(30, 3, 'Dictionaries store data as?', 'B', 'List items', 'Key-value pairs', 'Indexes', 'Tuples'),
(31, 3, 'Which function gets user input?', 'D', 'scan()', 'read()', 'get()', 'input()'),
(32, 3, 'Which keyword defines anonymous function?', 'A', 'lambda', 'func', 'anon', 'def'),
(33, 3, 'Which data type stores unique values?', 'C', 'list', 'tuple', 'set', 'string');

-- --------------------------------------------------------

--
-- Table structure for table `quizzes`
--

CREATE TABLE `quizzes` (
  `quiz_id` int(11) NOT NULL,
  `title` varchar(150) NOT NULL,
  `created_by` int(11) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `quizzes`
--

INSERT INTO `quizzes` (`quiz_id`, `title`, `created_by`, `created_at`) VALUES
(1, 'Java Basics Quiz', 1, '2026-02-06 14:01:58'),
(2, 'Java OOP & Advanced Quiz', 1, '2026-02-15 07:12:12'),
(3, 'Python Fundamentals Quiz', 1, '2026-02-15 07:12:12');

-- --------------------------------------------------------

--
-- Table structure for table `results`
--

CREATE TABLE `results` (
  `result_id` bigint(20) UNSIGNED NOT NULL,
  `student_id` int(11) NOT NULL,
  `quiz_id` int(11) NOT NULL,
  `score` int(11) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `results`
--

INSERT INTO `results` (`result_id`, `student_id`, `quiz_id`, `score`, `created_at`) VALUES
(1, 1, 1, 2, '2026-02-11 05:50:21'),
(2, 1, 1, 2, '2026-02-11 05:50:21'),
(3, 1, 1, 1, '2026-02-11 05:50:21'),
(4, 6, 1, 3, '2026-02-11 05:50:21'),
(5, 1, 1, 1, '2026-02-11 05:50:21'),
(6, 1, 1, 2, '2026-02-11 05:50:21'),
(7, 1, 1, 3, '2026-02-11 05:50:21'),
(8, 1, 1, 2, '2026-02-11 05:50:21'),
(9, 1, 1, 1, '2026-02-11 05:50:21'),
(10, 1, 1, 1, '2026-02-11 05:50:21');

-- --------------------------------------------------------

--
-- Table structure for table `students`
--

CREATE TABLE `students` (
  `student_id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `students`
--

INSERT INTO `students` (`student_id`, `name`, `email`, `password_hash`, `created_at`) VALUES
(1, 'pranjal ashok borde', 'pranjal95@gmail.com', 'scrypt:32768:8:1$nIYmN5nntKt8aELH$65041087b3c1d3f3cbc5a16202828edfa8bc8bf58fb867389ad5fd7fbce5cc003c7b1368460408ae773cd972f9d9aea16cffb9c8497765d9a02d90ba1ca5b255', '2026-02-06 13:03:56'),
(5, 'Sneha Ghule', 'sneha05@gmail.com', 'scrypt:32768:8:1$mQ57TV4Mow6AX0ND$ea9341b29393435e78c9fc543fcd2d1cba9c5eb34216673176a80db38d66c571c7af905959699f5b735c728bfb7fadc13b47e686e8e22cb482ed95861e565869', '2026-02-06 13:50:18'),
(6, 'Tanisha Bhosale', 'tanisha02@gmail.com', 'scrypt:32768:8:1$z8EtaiMhsJjAnaQf$72fae1e3a0e58df543a162ab1c59664dec5978af75e7b78f79cfb76ea17da67093167b68b5a91b8e5bd17ee40203d29db0a87961e42de29a1de0d0cd6e64bde4', '2026-02-07 05:36:39');

-- --------------------------------------------------------

--
-- Table structure for table `student_activity`
--

CREATE TABLE `student_activity` (
  `activity_id` bigint(20) UNSIGNED NOT NULL,
  `student_id` int(11) NOT NULL,
  `activity_type` varchar(50) NOT NULL,
  `description` text NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `student_activity`
--

INSERT INTO `student_activity` (`activity_id`, `student_id`, `activity_type`, `description`, `created_at`) VALUES
(1, 1, 'program', 'Practiced programming exercises', '2026-02-11 05:20:51'),
(2, 1, 'quiz', 'Completed quiz (Score: 1)', '2026-02-11 05:21:04'),
(3, 1, 'quiz', 'Completed quiz (Score: 1)', '2026-02-11 05:33:27'),
(4, 1, 'program', 'Practiced programming exercises', '2026-02-11 05:48:01');

-- --------------------------------------------------------

--
-- Table structure for table `student_quizzes`
--

CREATE TABLE `student_quizzes` (
  `student_id` int(11) NOT NULL,
  `quiz_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `student_quizzes`
--

INSERT INTO `student_quizzes` (`student_id`, `quiz_id`) VALUES
(1, 1);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admins`
--
ALTER TABLE `admins`
  ADD PRIMARY KEY (`admin_id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `flashcards`
--
ALTER TABLE `flashcards`
  ADD PRIMARY KEY (`flashcard_id`),
  ADD KEY `fk_flashcard_admin` (`created_by`);

--
-- Indexes for table `flashcard_activity`
--
ALTER TABLE `flashcard_activity`
  ADD PRIMARY KEY (`activity_id`),
  ADD KEY `fk_flashcard_student` (`student_id`),
  ADD KEY `fk_flashcard_card` (`flashcard_id`);

--
-- Indexes for table `programs`
--
ALTER TABLE `programs`
  ADD PRIMARY KEY (`program_id`),
  ADD KEY `fk_program_admin` (`created_by`);

--
-- Indexes for table `questions`
--
ALTER TABLE `questions`
  ADD PRIMARY KEY (`question_id`),
  ADD KEY `fk_question_quiz` (`quiz_id`);

--
-- Indexes for table `quizzes`
--
ALTER TABLE `quizzes`
  ADD PRIMARY KEY (`quiz_id`),
  ADD KEY `created_by` (`created_by`);

--
-- Indexes for table `results`
--
ALTER TABLE `results`
  ADD PRIMARY KEY (`result_id`),
  ADD KEY `fk_result_student` (`student_id`),
  ADD KEY `fk_result_quiz` (`quiz_id`);

--
-- Indexes for table `students`
--
ALTER TABLE `students`
  ADD PRIMARY KEY (`student_id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `student_activity`
--
ALTER TABLE `student_activity`
  ADD PRIMARY KEY (`activity_id`),
  ADD KEY `fk_activity_student` (`student_id`);

--
-- Indexes for table `student_quizzes`
--
ALTER TABLE `student_quizzes`
  ADD PRIMARY KEY (`student_id`,`quiz_id`),
  ADD KEY `fk_sq_quiz` (`quiz_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admins`
--
ALTER TABLE `admins`
  MODIFY `admin_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `flashcards`
--
ALTER TABLE `flashcards`
  MODIFY `flashcard_id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT for table `flashcard_activity`
--
ALTER TABLE `flashcard_activity`
  MODIFY `activity_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `programs`
--
ALTER TABLE `programs`
  MODIFY `program_id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=38;

--
-- AUTO_INCREMENT for table `questions`
--
ALTER TABLE `questions`
  MODIFY `question_id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=34;

--
-- AUTO_INCREMENT for table `quizzes`
--
ALTER TABLE `quizzes`
  MODIFY `quiz_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `results`
--
ALTER TABLE `results`
  MODIFY `result_id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `students`
--
ALTER TABLE `students`
  MODIFY `student_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `student_activity`
--
ALTER TABLE `student_activity`
  MODIFY `activity_id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `flashcards`
--
ALTER TABLE `flashcards`
  ADD CONSTRAINT `fk_flashcard_admin` FOREIGN KEY (`created_by`) REFERENCES `admins` (`admin_id`) ON DELETE CASCADE;

--
-- Constraints for table `flashcard_activity`
--
ALTER TABLE `flashcard_activity`
  ADD CONSTRAINT `fk_flashcard_card` FOREIGN KEY (`flashcard_id`) REFERENCES `flashcards` (`flashcard_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_flashcard_student` FOREIGN KEY (`student_id`) REFERENCES `students` (`student_id`) ON DELETE CASCADE;

--
-- Constraints for table `programs`
--
ALTER TABLE `programs`
  ADD CONSTRAINT `fk_program_admin` FOREIGN KEY (`created_by`) REFERENCES `admins` (`admin_id`) ON DELETE CASCADE;

--
-- Constraints for table `questions`
--
ALTER TABLE `questions`
  ADD CONSTRAINT `fk_question_quiz` FOREIGN KEY (`quiz_id`) REFERENCES `quizzes` (`quiz_id`) ON DELETE CASCADE;

--
-- Constraints for table `quizzes`
--
ALTER TABLE `quizzes`
  ADD CONSTRAINT `fk_quiz_admin` FOREIGN KEY (`created_by`) REFERENCES `admins` (`admin_id`) ON DELETE CASCADE;

--
-- Constraints for table `results`
--
ALTER TABLE `results`
  ADD CONSTRAINT `fk_result_quiz` FOREIGN KEY (`quiz_id`) REFERENCES `quizzes` (`quiz_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_result_student` FOREIGN KEY (`student_id`) REFERENCES `students` (`student_id`) ON DELETE CASCADE;

--
-- Constraints for table `student_activity`
--
ALTER TABLE `student_activity`
  ADD CONSTRAINT `fk_activity_student` FOREIGN KEY (`student_id`) REFERENCES `students` (`student_id`) ON DELETE CASCADE;

--
-- Constraints for table `student_quizzes`
--
ALTER TABLE `student_quizzes`
  ADD CONSTRAINT `fk_sq_quiz` FOREIGN KEY (`quiz_id`) REFERENCES `quizzes` (`quiz_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_sq_student` FOREIGN KEY (`student_id`) REFERENCES `students` (`student_id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
