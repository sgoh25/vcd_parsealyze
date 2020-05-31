library ieee;
context ieee.ieee_std_context;
use ieee.math_real;

entity ent is
  port (
    clk: in std_logic
  );
end entity;

architecture arch of ent is
  signal n_clk : std_logic;
  signal cnt: integer := -15;
  signal r: real := 0.0;
begin
  n_clk <= not clk;
  process(clk)
  begin
    if rising_edge(clk) then
      cnt <= cnt+1;
      r <= math_real.sqrt(real((15+cnt)/8)) + 0.75 * real(cnt);
    end if;
  end process;
end architecture;
