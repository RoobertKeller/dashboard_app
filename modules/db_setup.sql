-- Seleciona o schema
USE personal_finance;

-- Cria a tabela contas_a_pagar
CREATE TABLE IF NOT EXISTS contas_a_pagar (
    id INT PRIMARY KEY AUTO_INCREMENT,
    vencimento DATE NOT NULL,            
    beneficiario VARCHAR(100) NOT NULL,  
    descricao VARCHAR(255),              
    parcela VARCHAR(10),                 
    setor VARCHAR(50),                   
    valor DECIMAL(10,2) NOT NULL,        
    status VARCHAR(20) DEFAULT 'Pendente', 
    pago TINYINT(1) DEFAULT 0            
);

-- Trigger para atualizar status após INSERT
DELIMITER $$
CREATE TRIGGER atualiza_status_insert
AFTER INSERT ON contas_a_pagar
FOR EACH ROW
BEGIN
    UPDATE contas_a_pagar
    SET status = CASE
        WHEN NEW.pago = 1 THEN 'Pago'
        WHEN NEW.vencimento < CURDATE() THEN 'Atrasado'
        ELSE 'Em dia'
    END
    WHERE id = NEW.id;
END$$
DELIMITER ;

-- Trigger para atualizar status após UPDATE
DELIMITER $$
CREATE TRIGGER atualiza_status_update
AFTER UPDATE ON contas_a_pagar
FOR EACH ROW
BEGIN
    UPDATE contas_a_pagar
    SET status = CASE
        WHEN NEW.pago = 1 THEN 'Pago'
        WHEN NEW.vencimento < CURDATE() THEN 'Atrasado'
        ELSE 'Em dia'
    END
    WHERE id = NEW.id;
END$$
DELIMITER ;

-- Habilita o Event Scheduler (caso não esteja ativo)
SET GLOBAL event_scheduler = ON;

-- Evento diário para atualizar status automaticamente
CREATE EVENT IF NOT EXISTS atualizar_status_diario
ON SCHEDULE EVERY 1 DAY
STARTS CURRENT_TIMESTAMP  -- já começa a valer imediatamente
DO
  UPDATE contas_a_pagar
  SET status = CASE
      WHEN pago = 1 THEN 'Pago'
      WHEN vencimento < CURDATE() THEN 'Atrasado'
      ELSE 'Em dia'
  END;

CREATE TABLE IF NOT EXISTS contas_a_receber(
	id INT PRIMARY KEY AUTO_INCREMENT,
	vencimento DATE NOT NULL,
	pagador VARCHAR(15),
	descricao VARCHAR(15),
	valor DECIMAL(10,2) 
);

CREATE TABLE IF NOT EXISTS investimentos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    data DATE NOT NULL,                    
    ativo VARCHAR(20) NOT NULL,            
    preco_pago DECIMAL(10,2),              
    cotas DECIMAL(10,4),                   
    valor_total DECIMAL(12,2) NOT NULL     
);

