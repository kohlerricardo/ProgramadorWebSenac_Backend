-- emprestimo.categoria_equipamento definição

CREATE TABLE `categoria_equipamento` (
  `categoria_id` int(11) NOT NULL AUTO_INCREMENT,
  `categoria_descricao` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`categoria_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;


-- emprestimo.roles definição

CREATE TABLE `roles` (
  `roles_id` int(11) NOT NULL AUTO_INCREMENT,
  `roles_descricao` varchar(25) NOT NULL,
  PRIMARY KEY (`roles_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;


-- emprestimo.usuario definição

CREATE TABLE `usuario` (
  `usuario_id` int(11) NOT NULL AUTO_INCREMENT,
  `usuario_nome` varchar(100) NOT NULL,
  `usuario_sobrenome` varchar(100) NOT NULL,
  `usuario_email` varchar(100) DEFAULT NULL,
  `usuario_senha` varchar(255) NOT NULL,
  PRIMARY KEY (`usuario_id`),
  UNIQUE KEY `usuario_email` (`usuario_email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;


-- emprestimo.equipamento definição

CREATE TABLE `equipamento` (
  `equipamento_id` int(11) NOT NULL AUTO_INCREMENT,
  `equipamento_patrimonio` varchar(20) NOT NULL,
  `equipamento_categoria_equipamento_id` int(11) NOT NULL,
  `equipamento_descricao` varchar(255) NOT NULL,
  `equipamento_status_equipamento` enum('DISPONÍVEL','RESERVADO','EM MANUTENÇÃO','INDISPONÍVEL') DEFAULT 'DISPONÍVEL',
  PRIMARY KEY (`equipamento_id`),
  KEY `FK_equipamento_categoria_equipamento` (`equipamento_categoria_equipamento_id`),
  CONSTRAINT `FK_equipamento_categoria_equipamento` FOREIGN KEY (`equipamento_categoria_equipamento_id`) REFERENCES `categoria_equipamento` (`categoria_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;


-- emprestimo.usuario_has_role definição

CREATE TABLE `usuario_has_role` (
  `usuario_has_role_usuario_id` int(11) NOT NULL,
  `usuario_has_role_role_id` int(11) NOT NULL,
  PRIMARY KEY (`usuario_has_role_usuario_id`,`usuario_has_role_role_id`),
  KEY `usuario_has_role_role_id` (`usuario_has_role_role_id`),
  CONSTRAINT `1` FOREIGN KEY (`usuario_has_role_usuario_id`) REFERENCES `usuario` (`usuario_id`),
  CONSTRAINT `2` FOREIGN KEY (`usuario_has_role_role_id`) REFERENCES `roles` (`roles_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;


-- emprestimo.emprestimo definição

CREATE TABLE `emprestimo` (
  `emprestimo_id` int(11) NOT NULL AUTO_INCREMENT,
  `emprestimo_solicitante_id` int(11) NOT NULL,
  `emprestimo_aprovador_id` int(11) DEFAULT NULL,
  `emprestimo_equipamento_id` int(11) NOT NULL,
  `emprestimo_data_solicitacao` datetime NOT NULL DEFAULT current_timestamp(),
  `emprestimo_data_aprovacao` datetime DEFAULT NULL,
  `emprestimo_data_devolucao` datetime DEFAULT NULL,
  `emprestimo_demanda` text NOT NULL,
  `emprestimo_parecer` text DEFAULT NULL,
  `emprestimo_status_emprestimo` enum('PENDENTE','APROVADO','RECUSADO','FINALIZADO') DEFAULT 'PENDENTE',
  `emprestimo_data_devolucao_prevista` datetime DEFAULT NULL,
  PRIMARY KEY (`emprestimo_id`),
  KEY `FK_emprestimo_equipamento` (`emprestimo_equipamento_id`),
  KEY `FK_emprestimo_usuario_2` (`emprestimo_aprovador_id`),
  KEY `FK_emprestimo_usuario_3` (`emprestimo_solicitante_id`),
  CONSTRAINT `FK_emprestimo_equipamento` FOREIGN KEY (`emprestimo_equipamento_id`) REFERENCES `equipamento` (`equipamento_id`),
  CONSTRAINT `FK_emprestimo_usuario_2` FOREIGN KEY (`emprestimo_aprovador_id`) REFERENCES `usuario` (`usuario_id`),
  CONSTRAINT `FK_emprestimo_usuario_3` FOREIGN KEY (`emprestimo_solicitante_id`) REFERENCES `usuario` (`usuario_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;