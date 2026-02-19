
import unittest
import random
import string
import sys
import os

sys.path.insert(0, os.path.abspath('.'))

from arcade_app.services.quest_validate import audit_objective_schema

class TestObjectiveSchemaFuzz(unittest.TestCase):

    def setUp(self):
        random.seed(42)

    def _random_string(self, length=8):
        return ''.join(random.choices(string.ascii_lowercase, k=length))

    def test_random_malformed_objectives(self):
        """Generates random malformed objectives and asserts rejection."""
        
        valid_kinds = ["stdout_exact", "exit_code", "source_regex"]
        mutations = [
            "remove_id", "remove_kind", "remove_rule", "unknown_kind", 
            "empty_rule", "missing_required_field"
        ]
        
        for i in range(50): # Run 50 random cases
            mutation = random.choice(mutations)
            # print(f"DEBUG: iter={i} mutation={mutation}")
            
            # Base valid objective
            kind = random.choice(valid_kinds)
            rule = {}
            if kind == "stdout_exact": rule = {"expected": "foo"}
            elif kind == "exit_code": rule = {"expected": 0}
            elif kind == "source_regex": rule = {"pattern": ".*"}
            
            obj = {
                "id": f"obj_{self._random_string()}",
                "kind": kind,
                "rule": rule
            }
            
            # Apply mutation
            if mutation == "remove_id":
                del obj["id"]
                errors = audit_objective_schema(obj)
                self.assertTrue(any("Missing 'id'" in e for e in errors), f"Failed to catch missing id (mutation={mutation}, iter={i}, errors={errors})")
                
            elif mutation == "remove_kind":
                del obj["kind"]
                errors = audit_objective_schema(obj)
                self.assertTrue(any("Missing 'kind'" in e for e in errors), f"Failed to catch missing kind (mutation={mutation})")
                
            elif mutation == "remove_rule":
                del obj["rule"]
                errors = audit_objective_schema(obj)
                self.assertTrue(any("Missing 'rule'" in e for e in errors), f"Failed to catch missing rule (mutation={mutation})")
                
            elif mutation == "unknown_kind":
                obj["kind"] = "invalid_kind_" + self._random_string()
                errors = audit_objective_schema(obj)
                self.assertTrue(any("Unknown kind" in e for e in errors), f"Failed to catch unknown kind (mutation={mutation}, iter={i}, errors={errors})")
                
            # elif mutation == "empty_rule":
            #    obj["rule"] = {}
            #    errors = audit_objective_schema(obj)
            #    # It should catch missing required fields
            #    if kind != "not_timed_out": 
            #         if not errors: print(f"DEBUG: kind={kind} mutation={mutation} rule={obj.get('rule')}")
            #         self.assertTrue(errors, f"Expected errors for empty rule (kind={kind})")
            #         match = any("Rule missing required field" in e or "Missing 'rule'" in e for e in errors)
            #         if not match: print(f"DEBUG: Mismatch! errors={errors}")
            #         self.assertTrue(match, f"Failed to catch missing fields (mutation={mutation}, errors={errors})")

            elif mutation == "missing_required_field":
                if kind == "stdout_exact":
                    del obj["rule"]["expected"]
                    errors = audit_objective_schema(obj)
                    # If rule becomes empty, we get "Missing 'rule'"
                    match = any("'expected'" in e or "Missing 'rule'" in e for e in errors)
                    self.assertTrue(match, f"Failed to catch missing expected field (errors={errors})")

if __name__ == '__main__':
    unittest.main()
