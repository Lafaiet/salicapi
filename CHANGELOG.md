# Change Log
Todas alterações relevantes ocorridas nesse projeto serão documentadas nesse arquivo.

O formato de log é baseado em [Keep a Changelog](http://keepachangelog.com/) e o versionamento segue  a semântica [Semantic Versioning](http://semver.org/).

## [1.1.1-beta] - 2017-03-06
### Added
- Links **first** e **last** em consultas tipo lista
- URL's para consultas detalhadas de **proponentes**, **fornecedores** e **incentivadores** 
- Campos  `count` e `total` em consultas tipo lista

### Changed
- Links **prev** e **next** não mais aparecem em caso de primeira e última página, respectivamente
- Projetos são ordenados por **ano** em ordem **decrescente** 

### Fixed
- Link de **fornecedores** não faz mais distinção `fornecedores/` e `fornecedores`
- ```access_control_headers``` é enviado junto ao cabeçalho de retorno, explicitando os campos expostos pela API
- Readequação HAL em vários pontos
- Readequação de documentação SWAGGER


## [1.0.0-beta] - 2016-12-23

[1.0.0-beta]: https://github.com/Lafaiet/salicapi/releases/tag/v1.0.0-beta
[1.1.1-beta]: https://github.com/Lafaiet/salicapi/compare/v1.0.0-beta...v1.1.1-beta