// Sample Balancia actions
export async function getBalance(userId: string): Promise<number> {
  const response = await fetch('/api/balance/' + userId);
  const data = await response.json();
  return data.balance;
}

export async function transferFunds(fromId: string, toId: string, amount: number): Promise<boolean> {
  const response = await fetch('/api/transfer', {
    method: 'POST',
    body: JSON.stringify({ fromId, toId, amount })
  });
  return response.ok;
}
