import pytest
from lsprotocol.types import Position
from pygls.workspace.text_document import TextDocument

import server.server as server_module
from server.server import get_class_name_as_location, resolve_class_file


def make_document(source: str) -> TextDocument:
    return TextDocument(uri="file:///test.yaml", source=source)


def make_position(line: int, character: int) -> Position:
    return Position(line=line, character=character)


class TestGetClassNameAsLocation:
    def test_cursor_in_middle_of_dotted_class_name(self):
        doc = make_document("  - foo.bar\n")
        assert get_class_name_as_location(doc, make_position(0, 6)) == "foo.bar"

    def test_cursor_at_start_of_class_name(self):
        doc = make_document("  - foo.bar\n")
        assert get_class_name_as_location(doc, make_position(0, 4)) == "foo.bar"

    def test_cursor_at_end_of_class_name(self):
        doc = make_document("  - foo.bar\n")
        # position 10 is 'r', the last character of 'bar'
        assert get_class_name_as_location(doc, make_position(0, 10)) == "foo.bar"

    def test_cursor_at_start_of_line_returns_empty(self):
        doc = make_document("  - foo.bar\n")
        assert get_class_name_as_location(doc, make_position(0, 0)) == ""

    def test_simple_class_name(self):
        doc = make_document("  - common\n")
        assert get_class_name_as_location(doc, make_position(0, 6)) == "common"

    def test_cursor_on_second_line(self):
        doc = make_document("classes:\n  - foo.bar\n")
        assert get_class_name_as_location(doc, make_position(1, 6)) == "foo.bar"


@pytest.fixture()
def inventory(tmp_path, monkeypatch):
    """Set up a temporary inventory root and reset server globals after each test."""
    monkeypatch.setattr(server_module, "INVENTORY_PATH", tmp_path)
    monkeypatch.setattr(server_module, "YAML_EXTENSION", "yml")
    return tmp_path


class TestResolveClassFile:
    def test_empty_class_name_returns_none(self, inventory):
        assert resolve_class_file("", inventory) is None

    def test_nonexistent_class_returns_none(self, inventory):
        assert resolve_class_file("nonexistent", inventory) is None

    def test_simple_class_name_resolves_to_yml_file(self, inventory):
        classes_dir = inventory / "classes"
        classes_dir.mkdir()
        class_file = classes_dir / "common.yml"
        class_file.write_text("# class content")
        assert resolve_class_file("common", inventory) == class_file

    def test_dotted_class_name_resolves_to_nested_file(self, inventory):
        nested_dir = inventory / "classes" / "component"
        nested_dir.mkdir(parents=True)
        class_file = nested_dir / "myapp.yml"
        class_file.write_text("# component content")
        assert resolve_class_file("component.myapp", inventory) == class_file

    def test_directory_class_resolves_to_init_file(self, inventory):
        class_dir = inventory / "classes" / "base"
        class_dir.mkdir(parents=True)
        init_file = class_dir / "init.yml"
        init_file.write_text("# init content")
        assert resolve_class_file("base", inventory) == init_file

    def test_relative_class_name_resolves_from_document_dir(self, inventory):
        sibling_file = inventory / "sibling.yml"
        sibling_file.write_text("# sibling content")
        assert resolve_class_file(".sibling", inventory) == sibling_file

    def test_yaml_extension_is_used(self, inventory, monkeypatch):
        monkeypatch.setattr(server_module, "YAML_EXTENSION", "yaml")
        classes_dir = inventory / "classes"
        classes_dir.mkdir()
        class_file = classes_dir / "common.yaml"
        class_file.write_text("# class content")
        assert resolve_class_file("common", inventory) == class_file
