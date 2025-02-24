from pydantic import BaseModel


class SecrecyCliSecretsConfig(BaseModel):
    modules: set[str]

    # TODO: Also support plain files as an escape hatch?

    # @field_validator("modules")
    # @classmethod
    # def files_must_reference_importable_python_modules(
    #     cls, value: set[str]
    # ) -> set[str]:
    #     for module_specifier in value:
    #         try:
    #             import_module(module_specifier)
    #         except BaseException:
    #             raise ValueError(
    #                 f"'{module_specifier}' does not seem to be an importable Python module."
    #             )
    #     return value


class SecrecyCliConfig(BaseModel):
    secrets: SecrecyCliSecretsConfig

    @classmethod
    def default(cls) -> "SecrecyCliConfig":
        return SecrecyCliConfig(secrets=SecrecyCliSecretsConfig(modules=set()))
