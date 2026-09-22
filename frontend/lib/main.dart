import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'AHTX Predictor',
      theme: ThemeData.dark(),
      home: const PredictorScreen(),
    );
  }
}

class PredictorScreen extends StatefulWidget {
  const PredictorScreen({super.key});

  @override
  State<PredictorScreen> createState() => _PredictorScreenState();
}

class _PredictorScreenState extends State<PredictorScreen> {
  final TextEditingController _problemController = TextEditingController();
  final TextEditingController _customTagsController = TextEditingController();
  final TextEditingController _customMethodsController = TextEditingController();
  
  List<dynamic> predictedTags = [];
  List<dynamic> predictedMethods = [];
  List<dynamic> allAvailableTags = [];
  List<dynamic> allAvailableMethods = [];
  
  final Set<String> selectedFeedbackTags = {};
  final Set<String> selectedFeedbackMethods = {};

  bool isLoading = false;
  bool canSolve = true;
  String errorMessage = "";
  bool showFeedbackSection = false;

  Future<void> predictProblem() async {
    if (_problemController.text.trim().isEmpty) return;

    setState(() {
      isLoading = true;
      predictedTags = [];
      predictedMethods = [];
      errorMessage = "";
      showFeedbackSection = false;
      selectedFeedbackTags.clear();
      selectedFeedbackMethods.clear();
      _customTagsController.clear();
      _customMethodsController.clear();
    });

    try {
      final response = await http.post(
        Uri.parse('http://127.0.0.1:8000/predict'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'text': _problemController.text}),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        setState(() {
          canSolve = data['can_solve'] ?? true;
          allAvailableTags = data['all_tags'] ?? [];
          allAvailableMethods = data['all_methods'] ?? [];
          
          predictedTags = data['predicted_tags'] ?? [];
          predictedMethods = data['predicted_methods'] ?? [];

          selectedFeedbackTags.addAll(predictedTags.map((e) => e.toString()));
          selectedFeedbackMethods.addAll(predictedMethods.map((e) => e.toString()));

          if (!canSolve) {
            errorMessage = "Can't solve! Please adjust the tags & methods below.";
            showFeedbackSection = true;
          } else {
            showFeedbackSection = false;
          }
        });
      } else {
        setState(() {
          errorMessage = "Server error occurred!";
        });
      }
    } catch (e) {
      setState(() {
        errorMessage = "Failed to connect to backend: $e";
      });
    } finally {
      setState(() {
        isLoading = false;
      });
    }
  }

  Future<void> sendFeedback() async {
    // دمج الاختيارات مع أي كتابة حرة إضافية كتبها المستخدم
    Set<String> finalTags = Set.from(selectedFeedbackTags);
    if (_customTagsController.text.trim().isNotEmpty) {
      final extraTags = _customTagsController.text.split(',').map((e) => e.trim()).where((e) => e.isNotEmpty);
      finalTags.addAll(extraTags);
    }

    Set<String> finalMethods = Set.from(selectedFeedbackMethods);
    if (_customMethodsController.text.trim().isNotEmpty) {
      final extraMethods = _customMethodsController.text.split(',').map((e) => e.trim()).where((e) => e.isNotEmpty);
      finalMethods.addAll(extraMethods);
    }

    String tagsString = finalTags.isNotEmpty ? finalTags.join(', ') : "Greedy";
    String methodsString = finalMethods.isNotEmpty ? finalMethods.join(', ') : "Brute Force";

    try {
      final response = await http.post(
        Uri.parse('http://127.0.0.1:8000/feedback'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'text': _problemController.text,
          'true_tags': tagsString,
          'true_methods': methodsString,
        }),
      );

      if (response.statusCode == 200) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Feedback saved & Model retrained successfully! 🚀')),
        );
        setState(() {
          showFeedbackSection = false;
          predictProblem();
        });
      }
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error sending feedback: $e')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('AHTX - Tags & Methods Predictor'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: ListView(
          children: [
            TextField(
              controller: _problemController,
              maxLines: 4,
              decoration: const InputDecoration(
                labelText: 'Enter problem description...',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 16),
            ElevatedButton(
              onPressed: isLoading ? null : predictProblem,
              child: isLoading
                  ? const CircularProgressIndicator(color: Colors.white)
                  : const Text('Predict Tags & Methods'),
            ),
            const SizedBox(height: 24),
            
            if (errorMessage.isNotEmpty)
              Text(
                errorMessage,
                style: const TextStyle(color: Colors.redAccent, fontSize: 16, fontWeight: FontWeight.bold),
              ),

            const SizedBox(height: 16),
            if (predictedTags.isNotEmpty || predictedMethods.isNotEmpty) ...[
              const Text('Predicted Tags:', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
              const SizedBox(height: 8),
              Wrap(
                spacing: 8,
                runSpacing: 4,
                children: predictedTags.map((tag) => Chip(
                  label: Text(tag),
                  backgroundColor: Colors.blue.shade900,
                )).toList(),
              ),
              const SizedBox(height: 16),
              const Text('Predicted Methods:', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
              const SizedBox(height: 8),
              Wrap(
                spacing: 8,
                runSpacing: 4,
                children: predictedMethods.map((method) => Chip(
                  label: Text(method),
                  backgroundColor: Colors.teal.shade800,
                )).toList(),
              ),
              const SizedBox(height: 20),
              ElevatedButton.icon(
                style: ElevatedButton.styleFrom(backgroundColor: Colors.orange),
                onPressed: () {
                  setState(() {
                    showFeedbackSection = !showFeedbackSection;
                  });
                },
                icon: const Icon(Icons.edit),
                label: const Text('Modify Tags / Methods (Feedback)'),
              ),
            ],

            if (showFeedbackSection) ...[
              const Divider(height: 40),
              const Text('Adjust Tags (Tap to add/remove):', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
              const SizedBox(height: 8),
              Wrap(
                spacing: 6,
                children: allAvailableTags.map((tag) {
                  final isSelected = selectedFeedbackTags.contains(tag);
                  return FilterChip(
                    label: Text(tag),
                    selected: isSelected,
                    onSelected: (selected) {
                      setState(() {
                        if (selected) {
                          selectedFeedbackTags.add(tag);
                        } else {
                          selectedFeedbackTags.remove(tag);
                        }
                      });
                    },
                  );
                }).toList(),
              ),
              const SizedBox(height: 12),
              TextField(
                controller: _customTagsController,
                decoration: const InputDecoration(
                  labelText: 'Or add custom tags (comma separated, e.g. data structures, greedy)',
                  border: OutlineInputBorder(),
                ),
              ),
              const SizedBox(height: 20),
              const Text('Adjust Methods (Tap to add/remove):', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
              const SizedBox(height: 8),
              Wrap(
                spacing: 6,
                children: allAvailableMethods.map((method) {
                  final isSelected = selectedFeedbackMethods.contains(method);
                  return FilterChip(
                    label: Text(method),
                    selected: isSelected,
                    onSelected: (selected) {
                      setState(() {
                        if (selected) {
                          selectedFeedbackMethods.add(method);
                        } else {
                          selectedFeedbackMethods.remove(method);
                        }
                      });
                    },
                  );
                }).toList(),
              ),
              const SizedBox(height: 12),
              TextField(
                controller: _customMethodsController,
                decoration: const InputDecoration(
                  labelText: 'Or add custom methods (comma separated)',
                  border: OutlineInputBorder(),
                ),
              ),
              const SizedBox(height: 20),
              ElevatedButton(
                style: ElevatedButton.styleFrom(backgroundColor: Colors.green),
                onPressed: sendFeedback,
                child: const Text('Save Adjustments & Retrain'),
              ),
            ],
          ],
        ),
      ),
    );
  }
}